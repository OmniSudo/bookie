import os

from database.connection import connect_to_database


def create(db):
    cursor = db.cursor()
    cursor.execute("""
    create table if not exists book
    (
        series integer
            constraint book_series_id_fk
                references series (id),
        book   integer,
        title  integer,
        constraint book_pk
            primary key (series, book)
    );
    """)
    cursor.close()


def get_books_in_filesystem(series_path: str) -> list:
    books = []
    for book in os.listdir(series_path):
        if not os.path.isdir(f"{series_path}/{book}"):
            continue

        split = book.split(' - ', 1)
        if len(split) < 2:
            continue
        try:
            i = int(split[0])
            if i == 0:
                continue

            has_sub_books = False
            for sub_book in os.listdir(f"{series_path}/{book}"):
                if (os.path.isdir(f"{series_path}/{book}/{sub_book}")):
                    has_sub_books = True
            if has_sub_books:
                get = get_books_in_filesystem(f"{series_path}/{book}")
                for sub_book in get:
                    books.append((sub_book[0], f"{split[1]} - {sub_book[1]}", sub_book[2]))
            else:
                books.append((i, split[1], f"{series_path}/{book}"))
        except ValueError:
            print(f"Skipping invalid directory: {book}")
    return books


def insert_book(db, series, book, title):
    sql = db.cursor()

    res = sql.execute("""
    SELECT title FROM book WHERE series = ? AND book = ?;
    """, (series, book))

    result = res.fetchone()
    if result is None:
        sql.execute("""
        INSERT INTO book (series, book, title) VALUES (?, ?, ?);
        """, (series, book, title))
    else:
        sql.execute("""
        UPDATE book SET title = ? WHERE series = ? AND book = ?;
        """, (title, series, book))
    sql.close()