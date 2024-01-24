from tracy.triangle import Triangle
from tracy.core.database import Database
from tracy.core.importer import Importer

class Bootloader(Triangle):
    def __get_core__(self):
        return self.parent

    core = property(__get_core__)

    def __init__(self, core: Triangle):
        super().__init__(parent=core, name=self.__class__.__name__)

    def do(self, args: Triangle) -> Triangle:
        print(f"Booting {args.data['name']}")
        self.core.database = Database(self.core)
        self.core.importer = Importer(self.core)
        print(f"Booted {args.data['name']}")

        return