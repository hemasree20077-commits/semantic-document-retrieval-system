from sentence_transformers import CrossEncoder
import numpy as np

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query, results):

    pairs = [(query, r["chunk_text"]) for r in results]

    scores = reranker.predict(pairs)

    for i, r in enumerate(results):
       r["rerank_score"] = float(1 / (1 + np.exp(-scores[i])))

    results = sorted(results, key=lambda x: x["rerank_score"], reverse=True)

    return results