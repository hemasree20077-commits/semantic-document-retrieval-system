import faiss
import os

def load_index():

    path = "faiss_index/book_index.faiss"

    if os.path.exists(path):

        print("Loading FAISS index from disk...")
        return faiss.read_index(path)

    else:
        return faiss.IndexFlatIP(384)  # simple index