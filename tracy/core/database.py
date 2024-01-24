import sqlite3

from tracy.triangle import Triangle

class Database(Triangle):
    def __init__(self, core: Triangle):
        super().__init__(core, self.__class__.__name__)
        self.core = core
        self.connection = sqlite3.connect('database.db')

    def do(self, args: Triangle) -> Triangle:
        sql = args.data['sql']['query'] if 'sql' in args.data else ';'
        sql_args = args.data['sql']['kwargs'] if 'sql' in args.data else {}

        cursor = self.connection.cursor()
        res = cursor.execute(sql, sql_args)

        rows = res.fetchall()
        cursor.close()

        # Get the column names
        if cursor.description is not None:
            col_names = [desc[0] for desc in cursor.description]

            # Convert each row into a dictionary
            val = [dict(zip(col_names, row)) for row in rows]
            args.data['sql']['result'] = val
            return args
        else:
            args.data['sql']['result'] = []
            return args
