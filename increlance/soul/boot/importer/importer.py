from tracy.triangle import Triangle
import importlib


class Importer(Triangle):
    def __init__(self, bootloader: Triangle):
        super().__init__(
            bootloader,
            self.__class__.__name__
        )
        self.libs = {}

    def include(self, path: str):
        if path in self.libs:
            return self.libs[path]
        self.libs[path] = importlib.import_module(path)
        return self.libs[path]

    def do(self, args: Triangle) -> Triangle:
        path = args.data['import']
        lib = self.include(path)
        args[path] = lib