from increlance.triangle import Triangle
from increlance.soul.boot.database.database import Database
from increlance.soul.boot.importer.importer import Importer
from increlance.soul.boot.types.types import Types

from increlance.body.body import Body
from increlance.mind.mind import Mind

from increlance.soul.behavior.tree import Tree


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

        self.init_soul()
        self.init_body()
        self.init_mind()

    def register_builtin_types(self):
        register_type = self.get('Types/register')
        register_type(Triangle)
        register_type(Tree)

    def init_body(self):
        root = self.root()
        root.body = Body(root)

        root.body.right_child = Triangle(
            root.body,
            'Input'
        )
        root.body.left_child = Triangle(
            root.body,
            'Output'
        )

        include = self.get('Importer/include')
        console = include(
            'increlance.body.input.text.console'
        )
        input_triangle = root.body.get('Input')
        input_triangle.right_child = Triangle(
            input_triangle,
            'Text'
        )
        input_triangle.right_child.top_child = console.Console(root.left_child)

    def init_mind(self):
        root = self.root()
        include = self.get('Importer/include')

        root.mind = Mind(root)

    def save(self):
        self.get('Database/tables/triangle/save')(self.root())

    def init_soul(self):
        self.right_child = Database(self)
        self.left_child = Importer(self)
        self.top_child = Types(self)

        include = self.get('Importer/include')
        table = include(
            'tables.triangle_table',
            'increlance.soul.boot.database.tables.triangle_table'
        )
        tables = self.get('Database/tables')
        tables.data['triangle'] = table.TriangleTable(tables)

        root = self.root()
        root.uuid = tables.data['triangle'].get_id(root)

        self.register_builtin_types()
