from tracy.triangle import Triangle


class Bootloader(Triangle):
    def __init__(self, core: Triangle):
        super().__init__(parent=core, name=self.__class__.__name__)
