import sys

from increlance.triangle import Triangle
from increlance.soul.boot.bootloader import Bootloader

class Soul(Triangle):
    def __init__(self, root: Triangle):
        super().__init__(
            root,
            self.__class__.__name__
        )

        self.top_child = Bootloader(self)
