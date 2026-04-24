import faiss
import numpy as np

def build_faiss_index(embeddings):
    vectors = np.array(embeddings).astype("float32")
    dimension = vectors.shape[1]

    index = faiss.IndexIDMap(faiss.IndexFlatIP(dimension))
    ids = np.arange(0, len(vectors)).astype("int64")
    index.add_with_ids(vectors, ids)

    return index