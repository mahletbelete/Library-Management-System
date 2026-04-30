import sqlite3

def get_connection():
    return sqlite3.connect("library.db")  


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # BOOKS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        category TEXT,
        available INTEGER DEFAULT 1,
        quantity INTEGER,
        pdf_path TEXT
    )
    """)

    # BORROW (UPDATED WITH DUE + PENALTY SUPPORT)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrow(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student TEXT,
        book_id INTEGER,
        issue_date TEXT,
        due_date TEXT,
        return_date TEXT
    )
    """)

    conn.commit()
    conn.close()