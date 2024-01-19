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

    def query(self, sql: str, **values) -> list[dict] | None:
        cursor = self.connection.cursor()
        values = {int(k): v for k, v in values.items()}
        try:
            res = cursor.execute(sql, values)

            # Fetch all rows
            rows = res.fetchall()

            # Get the column names
            col_names = [desc[0] for desc in cursor.description]

            # Convert each row into a dictionary
            return [dict(zip(col_names, row)) for row in rows]
        except Exception as e:
            # TODO: Handle exception using mind
            print(f'Failed to execute SQL query: {e}')
            return None
