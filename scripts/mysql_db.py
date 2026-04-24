import mysql.connector

def get_connection():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2006",
        database="semantic_library"
    )

    return conn