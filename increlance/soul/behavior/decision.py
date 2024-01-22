from types import FunctionType

from increlance.triangle import Triangle


class Decision(Triangle):
    def __init__(self, executable: FunctionType):
        super().__init__()
        self.executable = executable

        pass

    def true(self, tri: Triangle) -> Triangle:
        self.right_child = tri
        return self

    def false(self, tri: Triangle) -> Triangle:
        self.left_child = tri
        return self

    def do(self, args: Triangle) -> Triangle:
        res = self.executable(args)
        if isinstance(res, bool):
            return self.right_child if res else self.left_child

        if isinstance(res, Triangle):
            data = res.data
            # TODO
            pass

        return None  # executed but dunno what to do with result
