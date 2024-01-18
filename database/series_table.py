from database.connection import connect_to_database


def create(db) -> None:
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT
    )
    """)

    cursor.close()


def insert_series(db, title: str, author: str) -> int:
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT id from series WHERE title = ? AND author = ?
        """, (title, author)).fetchone()
    if res is not None:
        return res[0]

    cursor.execute("""
    INSERT INTO series (title, author) VALUES (?, ?)
    """, (title, author))

    res = cursor.execute("""
        SELECT id from series WHERE title = ? AND author = ?
        """, (title, author)).fetchone()

    cursor.close()

    if res is not None:
        return res[0]

    return -1
