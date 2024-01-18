from increlance.triangle import Triangle
import sqlite3 as sql


class Database(Triangle):
    connection: sql.Connection = None

    def __init__(self, soul: Triangle):
        super().__init__(
            soul,
            self.__class__.__name__
        )
        self.connection = sql.connect('increlance.db')

