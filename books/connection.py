import sqlite3


def connect_to_database():
    connection = sqlite3.connect('books.db')
    return connection
