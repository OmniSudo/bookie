from tracy.triangle import Triangle
from tracy.core.bootloader import Bootloader


class Core(Triangle):
    def __get_boot__(self):
        return self.top_child

    def __set_boot__(self, value: Bootloader ):
        self.top_child = value

    boot = property(__get_boot__, __set_boot__)

    def __init__(self, root: Triangle):
        super().__init__(root, "core", False)

    def do(self, args: Triangle) -> Triangle:
        self.boot = Bootloader(self)
        self.boot.do(args)

        return self