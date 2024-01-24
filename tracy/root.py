import sys

from tracy.triangle import Triangle
import tracy.core

class Root(Triangle):
    def __get_core__(self):
        return self.top_child

    def __set_core__(self, value: tracy.core.Core):
        self.top_child = value

    core = property(__get_core__, __set_core__)

    def __init__(self):
        super().__init__(
            parent=self,
            name=self.__class__.__name__,
            uuid=False
        )

    def do(self, args: Triangle | None) -> Triangle:
        args = Triangle(None, "Genesis")
        args.data['name'] = sys.argv[1] if len(sys.argv) > 1 else "Unknown"

        self.core = tracy.core.Core(self)
        res = self.core.do(args)
        while res is not None:
            res = res.do(args)
