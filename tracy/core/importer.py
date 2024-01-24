import importlib

from tracy.triangle import Triangle
from importlib import import_module

class Importer(Triangle):
    def __get_core__(self):
        return self.parent

    core = property(__get_core__)

    def __init__(self, core: Triangle):
        super().__init__(core, self.__class__.__name__)

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
        return args