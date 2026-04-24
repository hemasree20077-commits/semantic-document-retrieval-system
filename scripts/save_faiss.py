import faiss

def save_index(index):

    faiss.write_index(index, "faiss_index/book_index.faiss")

    print("FAISS index saved successfully.")