from typing import cast

from increlance.triangle import Triangle
from increlance.soul.boot.database.database import Database
from increlance.soul.boot.importer.importer import Importer
from increlance.soul.boot.types.types import Types

from increlance.body.body import Body
from increlance.mind.mind import Mind


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
        self.right_child = Database(self)
        self.left_child = Importer(self)
        self.top_child = Types(self)

        self_table = self.get('Importer/include')(
            'tables.triangle_table',
            'increlance.soul.boot.database.tables.triangle_table'
        )
        tables = self.get('Database/tables')
        tables.data['triangle'] = self_table.TriangleTable(tables)
        root = self.root()
        root.uuid = tables.data['triangle'].get_id(root)

        root.left_child = Body(root)

        # Init body

        root.right_child = Mind(root)


    def register_builtin_types(self):
        self.get('Types/register')(Triangle)

    def save(self):
        self.get('Database/tables/triangle/save')(self.root())
