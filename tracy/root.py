import sys

from tracy.triangle import Triangle
import tracy.core

class Root(Triangle):
    def __init__(self):
        super().__init__(
            parent=self,
            name=self.__class__.__name__,
            uuid=False
        )

    def do(self, args: Triangle | None) -> Triangle:
        args.data['name'] = sys.argv[1] if len(sys.argv) > 1 else "Tracy"
        tracy.core.Core(self).do(args)