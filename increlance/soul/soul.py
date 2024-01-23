from tracy.triangle import Triangle
from increlance.soul.boot.bootloader import Bootloader


class Soul(Triangle):
    def __get_boot__(self):
        return self.top_child

    def __set_boot__(self, value: Bootloader):
        self.top_child = value

    boot = property(__get_boot__, __set_boot__)

    def __init__(self, root: Triangle):
        super().__init__(
            root,
            self.__class__.__name__
        )

        self.boot = Bootloader(self)
