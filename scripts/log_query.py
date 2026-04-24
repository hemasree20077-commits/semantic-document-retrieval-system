from scripts.mysql_db import get_connection

def log_query(query, top_result):

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO search_history (query, top_book, top_page)
    VALUES (%s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            query,
            top_result["book_name"],
            top_result["page_number"]
        )
    )

    conn.commit()

    cursor.close()
    conn.close()