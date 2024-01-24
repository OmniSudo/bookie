from tracy.core.database import Database
from tracy.triangle import Triangle
from tracy.core.bootloader import Bootloader


class Core(Triangle):
    def __get_boot__(self):
        return self.center_child

    def __set_boot__(self, value: Bootloader):
        self.center_child = value

    boot = property(__get_boot__, __set_boot__)

    def __get_database__(self):
        return self.right_child

    def __set_database__(self, value: Database):
        self.right_child = value

    database = property(__get_database__, __set_database__)

    def __get_importer__(self):
        return self.left_child

    def __set_importer__(self, value: Database):
        self.left_child = value

    importer = property(__get_importer__, __set_importer__)

    def __init__(self, root: Triangle):
        super().__init__(root, "Core", False)
        root.core = self

    def do(self, args: Triangle) -> Triangle:
        self.boot = Bootloader(self)
        return self.boot.do(args)