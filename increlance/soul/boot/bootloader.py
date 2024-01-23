import sys

from tracy.triangle import Triangle
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

    def do(self, args: Triangle) -> Triangle:
        name = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
        print(f'Booting into "{name}"')

        self.init_soul()
        self.init_body()
        self.init_mind()
        self.init_root(self.root())

        root = self.root()
        root.do(self.create_thought(root=root))

        return self

    def __get_database__(self) -> Database:
        return self.right_child

    def __get_importer__(self) -> Importer:
        return self.left_child

    def __get_types__(self) -> Types:
        return self.top_child

    database = property(__get_database__)
    importer = property(__get_importer__)
    types = property(__get_types__)

    def init_soul(self):
        self.right_child = Database(self)
        self.left_child = Importer(self)
        self.top_child = Types(self)

    def init_body(self):
        root = self.root()
        root.body = Body(root)

    def init_mind(self):
        root = self.root()
        root.mind = Mind(root)

    def create_thought(self, **kwargs):
        thought = Triangle(self.soul, 'Thought')
        thought.data = kwargs
        return thought

    def init_root(self, root: Triangle):
        def do(args: Triangle) -> Triangle:
            return args

        root.do = do
        pass
