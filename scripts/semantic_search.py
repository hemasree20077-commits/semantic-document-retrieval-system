import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from scripts.fetch_chunks_mysql import fetch_chunk_by_id

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def search(query, index, top_k=20):

    # 🔥 encode query
    query_vector = model.encode([query])
    query_vector = np.array(query_vector).astype("float32")

    # 🔥 MUST normalize (THIS WAS MISSING)
    faiss.normalize_L2(query_vector)

    # search
    distances, indices = index.search(query_vector, top_k)
    print("Indices:", indices[0][:5])
    print("Scores:", distances[0][:5])

    results = []

    for rank, idx in enumerate(indices[0]):

        if idx == -1:
            continue

        chunk_id = int(idx)

        metadata = fetch_chunk_by_id(chunk_id)

        if metadata:
            metadata["similarity_score"] = float(distances[0][rank])
            results.append(metadata)

    return results