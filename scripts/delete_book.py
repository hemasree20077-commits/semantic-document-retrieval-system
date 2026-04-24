import os
import numpy as np

from scripts.mysql_db import get_connection
from scripts.fetch_all_chunks_mysql import fetch_all_chunks
from scripts.create_embeddings import generate_embeddings
from scripts.build_faiss import build_faiss_index
from scripts.save_faiss import save_index


def delete_book(book_name):

    conn = get_connection()
    cursor = conn.cursor()

    # delete chunks from database
    cursor.execute(
        "DELETE FROM chunks WHERE book_name=%s",
        (book_name,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    # delete PDF file
    pdf_path = f"books/{book_name}"

    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    # rebuild FAISS index
    chunks = fetch_all_chunks()

    embeddings = generate_embeddings(chunks)

    index = build_faiss_index(embeddings)

    save_index(index)

    return True