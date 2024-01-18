from increlance.triangle import Triangle
from increlance.soul.database import Database


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
        self.soul.right_child = Database(self.soul)
