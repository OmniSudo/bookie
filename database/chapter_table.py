from database.connection import connect_to_database


def create(db) -> None:
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chapter (
        series INTEGER NOT NULL
            constraint word_series_id_fk
                references series (id),
        book INTEGER NOT NULL
            constraint word_book_id_fk
                references book (id),
        chapter INTEGER NOT NULL,
        title TEXT,
        constraint word_pk
            primary key (series, book, chapter)
        );
    """)
    cursor.close()


def insert_chapter(db, series, book, chapter, title) -> None:
    sql = db.cursor()

    res = sql.execute("""
        SELECT title FROM chapter WHERE series = ? AND book = ? AND chapter = ?;
        """, (series, book, chapter))

    result = res.fetchone()
    if result is None:
        sql.execute("""
            INSERT INTO chapter (series, book, chapter, title) VALUES (?, ?, ?, ?);
            """, (series, book, chapter, title))
    else:
        sql.execute("""
            UPDATE chapter SET title = ? WHERE series = ? AND book = ? AND chapter = ?;
            """, (title, series, book, chapter))
    sql.close()