from increlance.triangle import Triangle


class Soul(Triangle):
    def __init__(self, root: Triangle):
        super().__init__(
            root,
            self.__class__.__name__
        )
