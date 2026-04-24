from scripts.mysql_db import get_connection


def get_library_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(DISTINCT book_name) FROM chunks")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM chunks")
    total_chunks = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total_books, total_chunks