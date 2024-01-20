from increlance.soul import *
from increlance.mind import *
from increlance.body import *

from increlance.triangle import Triangle


class Self(Triangle):
    def __get__soul__(self):
        return self.top_child

    def __set__soul__(self, soul: Soul):
        self.top_child = soul

    # The 'kernel' of the self.
    # has records of behavioural data
    # has boot loader
    # has access to file system
    soul = property(__get__soul__, __set__soul__)

    def __get__mind__(self):
        return self.right_child

    def __set__mind__(self, mind: Mind):
        self.right_child = mind

    # Thinking / processing center of the Self
    mind = property(__get__mind__, __set__mind__)

    def __get__body__(self):
        return self.left_child

    def __set__body__(self, body: Body):
        self.left_child = body

    # Any peripherals that may be attached to the Self
    body = property(__get__body__, __set__body__)

    def __init__(self, name: str = None):
        super().__init__(
            self,
            name,
            {
                'u': 'soul',
                'l': 'mind',
                'r': 'body',
                'c': 'c'
            }
        )

        self.soul = Soul(self)
        self.get(f'/Soul/Bootloader/boot')(name)
        self.save()

