from scripts.mysql_db import get_connection

def fetch_chunk_by_id(faiss_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM chunks WHERE faiss_id = %s"

    cursor.execute(query, (faiss_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result