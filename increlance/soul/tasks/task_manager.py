from increlance.triangle import Triangle

class TaskManager(Triangle):
    def __init__(self, soul: Triangle):
        super().__init__(
            soul,
            self.__class__.__name__
        )