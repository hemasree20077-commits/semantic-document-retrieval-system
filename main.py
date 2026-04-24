from scripts.pdf_reader import read_pdfs
from scripts.chunk_text import chunk_documents
from scripts.store_chunks_mysql import store_chunks
from scripts.create_embeddings import generate_embeddings
from scripts.build_faiss import build_faiss_index
from scripts.save_faiss import save_index
from scripts.search_pipeline import search_pipeline
from scripts.mysql_db import get_connection


# -----------------------------
# Answer extraction
# -----------------------------
def extract_answer(text, query):
    text = text.replace("\n", " ").strip()
    sentences = text.split(". ")
    query_words = query.lower().split()

    scored_sentences = []
    for s in sentences:
        score = sum(1 for w in query_words if w in s.lower())
        if len(s.split()) > 5:
            scored_sentences.append((score, s))

    scored_sentences.sort(reverse=True, key=lambda x: x[0])
    top_sentences = [s for score, s in scored_sentences[:2]]

    if top_sentences:
        return ". ".join(top_sentences)

    return sentences[0] if sentences else text


# -----------------------------
# Reset MySQL chunks
# -----------------------------
def clear_chunks_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chunks")
    conn.commit()
    cursor.close()
    conn.close()
    print("Old chunks deleted from MySQL.")


# -----------------------------
# Build full pipeline
# -----------------------------
print("Loading PDFs...")
docs = read_pdfs("books")
print("Total pages loaded:", len(docs))

print("\nChunking text...")
chunks = chunk_documents(docs)
print("Total chunks created:", len(chunks))

print("\nClearing old MySQL chunks...")
clear_chunks_table()

print("\nStoring chunks in MySQL...")
store_chunks(chunks, start_id=0)

print("\nGenerating embeddings...")
vectors = generate_embeddings(chunks)
print("Embeddings generated:", len(vectors))

print("\nBuilding FAISS index...")
index = build_faiss_index(vectors)
save_index(index)
print("Total vectors in FAISS:", index.ntotal)

print("\nSystem ready for search")

# -----------------------------
# Search loop
# -----------------------------
while True:
    query = input("\nAsk a question: ").strip()

    if not query:
        continue

    results = search_pipeline(query, index)

    print("\nTop results:\n")
    print("TOTAL RESULTS:", len(results))

    for r in results:
        print("Book:", r["book_name"])
        print("Page:", r["page_number"])
        print("Score:", round(r.get("rerank_score", 0), 3))

        answer = extract_answer(r["chunk_text"], query)
        print("Answer:", answer)

        print("-" * 60)