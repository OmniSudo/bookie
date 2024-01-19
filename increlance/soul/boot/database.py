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
        self.index['c'] = 'tables'
        self.center_child = Triangle(self, 'tables')

    def query(self, sql: str, **values) -> list[dict] | None:
        cursor = self.connection.cursor()
        try:
            res = None
            if values is not None:
                res = cursor.execute(sql, values)
            else:
                res = cursor.execute(sql)

            # Fetch all rows
            rows = res.fetchall()

            # Get the column names
            if cursor.description is not None:
                col_names = [desc[0] for desc in cursor.description]

                # Convert each row into a dictionary
                return [dict(zip(col_names, row)) for row in rows]
            else:
                return []
        except Exception as e:
            # TODO: Handle exception using mind
            print(f'Failed to execute SQL query: {e}')
            return None

    def load(self, table: str) -> Triangle | None:
        return None