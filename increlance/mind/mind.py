from tracy.triangle import Triangle


class Mind(Triangle):
    def __init__(self, root: Triangle):
        super().__init__(
            root,
            self.__class__.__name__
        )
