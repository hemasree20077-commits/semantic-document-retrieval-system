import streamlit as st
import os
import base64

from scripts.load_faiss import load_index
from scripts.search_pipeline import search_pipeline
from scripts.library_stats import get_library_stats
from scripts.get_books import get_books
from scripts.get_history import get_history
from scripts.book_hash import get_book_hash
from scripts.check_book_exists import book_exists
from scripts.index_new_book import index_new_book
from scripts.delete_book import delete_book


# -----------------------------
# Highlight query words
# -----------------------------
def highlight_text(text, query):
    words = query.lower().split()
    for w in words:
        text = text.replace(w, f"**{w}**")
        text = text.replace(w.capitalize(), f"**{w.capitalize()}**")
    return text


# -----------------------------
# Display PDF
# -----------------------------
def display_pdf(file_path, page):

    if not os.path.exists(file_path):
        st.error(f"❌ File not found: {file_path}")
        return

    with open(file_path, "rb") as f:
        pdf_bytes = f.read()

    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}#page={page}"
            width="100%"
            height="700px"
            type="application/pdf">
        </iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)


# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Semantic Library Search", layout="wide")

st.title("📚 Semantic Library Search")


# -----------------------------
# Stats
# -----------------------------
total_books, total_chunks = get_library_stats()

c1, c2 = st.columns(2)
c1.metric("📚 Total Books", total_books)
c2.metric("🧩 Total Chunks", total_chunks)


# -----------------------------
# Sidebar (FIXED KEY)
# -----------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["Search", "Books", "History", "Upload Book"],
    key="main_menu"
)


# -----------------------------
# Load FAISS
# -----------------------------
@st.cache_resource
def initialize_indexes():
    return load_index()

index = initialize_indexes()


# ======================================================
# SEARCH PAGE
# ======================================================
if menu == "Search":

    st.header("🔎 Search the Library")

    query = st.text_input("Ask a question about the books")

    if query:

        results = search_pipeline(query, index)

        st.subheader("Top Results")

        for i, r in enumerate(results):

            st.markdown(f"### 📄 {r['book_name']}")

            col1, col2 = st.columns(2)
            col1.write(f"📑 Page: {r['page_number']}")
            col2.write(f"📊 Score: {round(r.get('rerank_score', 0), 3)}")

            highlighted = highlight_text(r["chunk_text"][:500], query)
            st.markdown(highlighted)

            # ✅ HANDLE BOTH PATHS
            path1 = os.path.join("books", r["book_name"])
            path2 = os.path.join("static", "books", r["book_name"])

            if os.path.exists(path1):
                pdf_path = path1
            elif os.path.exists(path2):
                pdf_path = path2
            else:
                pdf_path = None

            state_key = f"pdf_{i}"

            if st.button(f"📖 Open PDF - Page {r['page_number']}", key=f"btn_{i}"):
                st.session_state[state_key] = (pdf_path, r["page_number"])

            if state_key in st.session_state:
                path, page = st.session_state[state_key]

                if path:
                    display_pdf(path, page)
                else:
                    st.error("PDF not found")

            # DOWNLOAD
            if pdf_path:
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "⬇ Download PDF",
                        data=f,
                        file_name=r["book_name"],
                        mime="application/pdf",
                        key=f"download_{i}"
                    )

            st.markdown("---")


# ======================================================
# BOOKS PAGE
# ======================================================
elif menu == "Books":

    st.header("📚 Books in Library")

    books = get_books()

    for b in books:

        col1, col2 = st.columns([6, 1])

        col1.write(f"📄 {b}")

        if col2.button("🗑 Delete", key=f"delete_{b}"):

            with st.spinner("Deleting..."):
                delete_book(b)

            st.success(f"{b} deleted")

            st.cache_resource.clear()
            st.rerun()


# ======================================================
# HISTORY PAGE
# ======================================================
elif menu == "History":

    st.header("📜 Search History")

    history = get_history()

    for h in history:
        st.write(f"{h[1]} — {h[0]}")


# ======================================================
# UPLOAD PAGE
# ======================================================
elif menu == "Upload Book":

    st.header("➕ Upload New Book")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:

        save_path = os.path.join("books", uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        book_hash = get_book_hash(save_path)

        if book_exists(book_hash):
            st.warning("Book already exists")
        else:
            with st.spinner("Indexing..."):
                chunks = index_new_book(save_path, book_hash)

            st.success(f"Indexed {chunks} chunks")

            st.cache_resource.clear()
            st.rerun()