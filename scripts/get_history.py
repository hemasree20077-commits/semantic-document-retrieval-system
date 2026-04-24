from scripts.mysql_db import get_connection


def get_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT query, created_at
        FROM search_history
        ORDER BY created_at DESC
        LIMIT 20
    """)

    history = cursor.fetchall()

    cursor.close()
    conn.close()

    return history