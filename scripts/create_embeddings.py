from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = text.replace("\x00", "")
    text = text.encode("utf-8", "ignore").decode("utf-8")
    return text.strip()


def generate_embeddings(chunks):

    texts = []

    # 🔥 CLEAN CHUNKS IN-PLACE (IMPORTANT)
    for c in chunks:

        cleaned = clean_text(c.get("chunk_text", ""))

        if cleaned == "":
            cleaned = " "

        c["chunk_text"] = cleaned   # ✅ sync with DB

        texts.append(cleaned)

    embeddings = model.encode(texts, show_progress_bar=True)

    embeddings = np.array(embeddings).astype("float32")

    faiss.normalize_L2(embeddings)

    return embeddings