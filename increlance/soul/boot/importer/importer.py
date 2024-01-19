from increlance.triangle import Triangle
import importlib


class Importer(Triangle):
    def __init__(self, bootloader: Triangle):
        super().__init__(
            bootloader,
            self.__class__.__name__
        )
        self.libs = {}

    def include(self, name: str, path: str):
        if name in self.libs:
            return self.libs[name]
        self.libs[name] = importlib.import_module(path)
        return self.libs[name]

