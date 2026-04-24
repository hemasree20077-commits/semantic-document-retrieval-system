from scripts.mysql_db import get_connection


def book_exists(book_hash):

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id FROM chunks WHERE book_hash = %s LIMIT 1"

    cursor.execute(query, (book_hash,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None