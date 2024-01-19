import uuid

from increlance.triangle import Triangle
from increlance.soul.boot.database import Database
from increlance.soul.boot.importer import Importer


class Bootloader(Triangle):
    soul: Triangle = None

    def __init__(self, soul: Triangle):
        super().__init__(
            soul,
            self.__class__.__name__
        )
        self.soul = soul

    def boot(self, name: str = None):
        print(f'Booting into "{name}"')
        self.right_child = Database(self.soul)
        self.left_child = Importer(self.soul)

        self_table = self.get('Importer/include')('tables.self_table', 'increlance.soul.boot.tables.self_table')
        tables = self.get('Database/tables')
        tables.data['self_table'] = self_table.SelfTable(tables)
        root = self.root()
        root.uuid = tables.data['self_table'].get_triangle_id(root)

    def save(self):
        self.get('Database/tables/self_table/save_triangle')(self.root())