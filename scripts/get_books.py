from scripts.mysql_db import get_connection


def get_books():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT book_name FROM chunks")

    books = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return books