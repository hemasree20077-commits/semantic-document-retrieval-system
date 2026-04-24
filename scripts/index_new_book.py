import os
import numpy as np
from pypdf import PdfReader

from scripts.chunk_text import chunk_documents
from scripts.create_embeddings import generate_embeddings
from scripts.load_faiss import load_index
from scripts.save_faiss import save_index
from scripts.store_chunks_mysql import store_chunks


def index_new_book(book_path, book_hash):
    reader = PdfReader(book_path)

    docs = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        docs.append({
            "book_hash": book_hash,
            "book_name": os.path.basename(book_path),
            "page_number": i + 1,
            "text": text
        })

    chunks = chunk_documents(docs)
    vectors = generate_embeddings(chunks)

    index = load_index()
    start_id = index.ntotal
    ids = np.arange(start_id, start_id + len(vectors)).astype("int64")

    store_chunks(chunks, start_id)
    index.add_with_ids(vectors, ids)
    save_index(index)

    print("FAISS total:", index.ntotal)

    return len(chunks)