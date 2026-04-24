# 📚 Semantic Document Retrieval System

A semantic search system that allows users to search across PDF documents based on meaning rather than exact keywords.

## 🔍 Problem Statement

Traditional search systems rely on keyword matching, which fails when the query wording differs from the document text.

Example:

* Query: "learning from data"
* Document: "machine learning"

Keyword search fails ❌
Semantic search works ✔

## 🚀 Features

* Semantic search using embeddings
* Fast similarity search using FAISS
* MySQL database for metadata storage
* Cross-encoder reranking for better accuracy
* Streamlit-based user interface
* Dynamic PDF upload
* Search history tracking
* Book management (add/delete)

## 🧠 Tech Stack

* Python
* FAISS (Vector Database)
* Sentence Transformers (MiniLM)
* Cross-Encoder (MS MARCO MiniLM)
* MySQL
* Streamlit

## ⚙️ System Workflow

1. Extract text from PDFs using PyPDF
2. Split text into smaller chunks
3. Convert chunks into embeddings using MiniLM
4. Store embeddings in FAISS
5. Store metadata (text, page, book) in MySQL
6. Convert user query into embedding
7. Retrieve similar chunks using FAISS
8. Rerank results using cross-encoder
9. Display results in UI

## 🖥️ How to Run the Project

### Step 1: Install dependencies

pip install -r requirements.txt

### Step 2: Run the application

streamlit run app.py

## 📁 Project Structure

semantic-document-retrieval-system/

│── app.py
│── main.py
│── requirements.txt
│── .gitignore

│── scripts/
│   ├── chunk_text.py
│   ├── create_embeddings.py
│   ├── semantic_search.py
│   ├── search_pipeline.py
│   ├── rerank_results.py
│   ├── mysql_db.py
│   ├── pdf_reader.py
│   └── ...

## 🗄️ Data Storage

* FAISS → Stores embeddings (vectors)
* MySQL → Stores metadata (text, book name, page number)

## ⚠️ Limitations

* Mapping between FAISS and MySQL is index-based
* Not optimized for very large datasets
* Does not generate answers (retrieval only)
* Limited filtering and search customization

## 🔮 Future Improvements

* Improve FAISS–MySQL mapping using ID-based linking
* Optimize database queries
* Add FastAPI backend and React frontend
* Integrate LLM (RAG system)
* Add filters and advanced search

## 👤 Author

Hemasree L

## 📌 Summary

This project demonstrates how semantic search improves document retrieval by understanding meaning using embeddings instead of relying on keyword matching.
