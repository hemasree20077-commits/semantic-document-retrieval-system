from scripts.semantic_search import search
from scripts.rerank_results import rerank
from scripts.mysql_db import get_connection


# -----------------------------
# Store search history
# -----------------------------
def store_search_history(query):

    conn = get_connection()
    cursor = conn.cursor()

    query_sql = "INSERT INTO search_history (query) VALUES (%s)"
    cursor.execute(query_sql, (query,))

    conn.commit()

    cursor.close()
    conn.close()


# -----------------------------
# Search Pipeline
# -----------------------------
def search_pipeline(query, index):

    # 🔥 Step 1: semantic search
    results = search(query, index)

    if not results:
        return []

    # 🔥 Step 2: rerank (important)
    results = rerank(query, results)

    # 🔥 Step 3: filter bad results (optional but useful)
    results = sorted(results, key=lambda x: x.get("rerank_score", 0), reverse=True)

    # 🔥 Step 4: save history
    try:
        store_search_history(query)
    except:
        pass  # avoid crash if DB fails

    # 🔥 Step 5: return top results
    return results[:5]