import os
from pypdf import PdfReader
from scripts.hash_utils import generate_book_hash

def read_pdfs(folder_path):

    documents = []

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            file_path = os.path.join(folder_path, file)

            book_hash = generate_book_hash(file_path)

            reader = PdfReader(file_path)

            for page_num, page in enumerate(reader.pages):

                text = page.extract_text()

                documents.append({
                    "book_hash": book_hash,
                    "book_name": file,
                    "page_number": page_num + 1,
                    "text": text
                })

    return documents