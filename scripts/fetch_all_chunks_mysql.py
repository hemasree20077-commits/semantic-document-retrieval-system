from scripts.mysql_db import get_connection


def fetch_all_chunks():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT id, book_hash, book_name, page_number, chunk_text
    FROM chunks
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows