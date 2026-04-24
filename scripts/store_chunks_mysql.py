from scripts.mysql_db import get_connection


# -----------------------------
# Clean text before inserting
# -----------------------------
def clean_text(text):

    if not isinstance(text, str):
        return ""

    # 🔥 remove null bytes (MAIN FIX)
    text = text.replace("\x00", "")

    # remove invalid/unicode issues
    text = text.encode("utf-8", "ignore").decode("utf-8")

    return text.strip()


# -----------------------------
# Store chunks
# -----------------------------
def store_chunks(chunks, start_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO chunks (faiss_id, book_hash, book_name, page_number, chunk_text)
    VALUES (%s, %s, %s, %s, %s)
    """

    data = []

    for i, c in enumerate(chunks):

        text = clean_text(c.get("chunk_text", ""))

        # skip empty / invalid text
        if text == "":
            continue

        data.append((
            start_id + i,
            c.get("book_hash"),
            c.get("book_name"),
            c.get("page_number"),
            text
        ))

    if not data:
        print("No valid chunks to insert.")
        return

    cursor.executemany(query, data)
    conn.commit()

    cursor.close()
    conn.close()

    print(f"Chunks stored in MySQL successfully. Total inserted: {len(data)}")