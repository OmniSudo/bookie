from database.connection import connect_to_database


def create(db):
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS word (
        series INTEGER NOT NULL
            constraint word_series_id_fk
                references series (id),
        book INTEGER NOT NULL
            constraint word_book_id_fk
                references book (id),
        chapter INTEGER NOT NULL
            constraint word_chapter_id_fk
                references chapter (id),
        word INTEGER NOT NULL, 
        text TEXT,
        constraint word_pk
            primary key (series, book, chapter, word)
        )
    """)
    cursor.close()


def insert_word(db, series, book, chapter, word, text):
    sql = db.cursor()

    res = sql.execute("""
            SELECT text FROM word WHERE series = ? AND book = ? AND chapter = ? AND word = ?;
            """, (series, book, chapter, word))

    result = res.fetchone()
    if result is None:
        sql.execute("""
                INSERT INTO word (series, book, chapter, word, text) VALUES (?, ?, ?, ?, ?);
                """, (series, book, chapter, word, text))
    else:
        sql.execute("""
                UPDATE word SET text = ? WHERE series = ? AND book = ? AND chapter = ? AND word = ?;
                """, (text, series, book, chapter, word))
    sql.close()
