from __future__ import annotations

from inspect import signature
import uuid as id
import types


class Triangle:
    def __get_uuid__(self) -> id.UUID | None:
        return self.__uuid__

    def __set_uuid__(self, value: str | id.UUID) -> None:
        if isinstance(value, str):
            value = id.UUID(value)

        if isinstance(value, id.UUID):
            old = self.__uuid__
            self.__uuid__ = value
            if old is not None:
                self.get('/Soul/Bootloader/Database/tables/triangle/change')(old, self.__get_uuid__())

    def __get_parent__(self) -> Triangle:
        return self.__parent__

    def __set_parent__(self, value: Triangle | str | id.UUID) -> None:
        if isinstance(value, str):
            value = self.get(value)
        if isinstance(value, id.UUID):
            # TODO: Repalce with something like /Mind/find/by_uuid?uuid={value}
            value = self.get(f'/Soul/Bootloader/Database/tables/self/{value}')

        if isinstance(value, Triangle):
            self.__parent__ = value

    def __get_center_child__(self) -> Triangle:
        return self.__center_child__

    def __set_center_child__(self, value: Triangle):
        if self.__center_child__ is not None:
            self.__center_child__.parent = None
        self.__center_child__ = value
        if value is not None:
            value.parent = self

    def __get_top_child__(self) -> Triangle:
        return self.__top_child__

    def __set_top_child__(self, value: Triangle):
        if self.__top_child__ is not None:
            self.__top_child__.parent = None
        self.__top_child__ = value
        if value is not None:
            value.parent = self

    def __get_left_child__(self) -> Triangle:
        return self.__left_child__

    def __set_left_child__(self, value: Triangle):
        if self.__left_child__ is not None:
            self.__left_child__.parent = None
        self.__left_child__ = value
        if value is not None:
            value.parent = self

    def __get_right_child__(self) -> Triangle:
        return self.__right_child__

    def __set_right_child__(self, value: Triangle):
        if self.__right_child__ is not None:
            self.__right_child__.parent = None
        self.__right_child__ = value
        if value is not None:
            value.parent = self

    name: str = None
    uuid = property(__get_uuid__, __set_uuid__)
    parent = property(__get_parent__, __set_parent__)

    center_child: Triangle = property(__get_center_child__, __set_center_child__)

    top_child: Triangle = property(__get_top_child__, __set_top_child__)
    left_child: Triangle = property(__get_left_child__, __set_left_child__)
    right_child: Triangle = property(__get_right_child__, __set_right_child__)

    __uuid__: uuid = None
    __parent__: Triangle = None

    __center_child__: Triangle = None

    __top_child__: Triangle = None
    __left_child__: Triangle = None
    __right_child__: Triangle = None

    def __init__(
            self,
            parent: Triangle = None,
            name: str = '',
            uuid: bool | id.UUID = False,
    ):
        self.parent = parent
        self.name = name

        if isinstance(uuid, id.UUID):
            self.__uuid__ = uuid
        elif uuid:
            self.uuid = id.uuid4()

    def __eq__(self, other):
        if not isinstance(other, Triangle): return False

        # TODO: Equality from root triangle equality function

        return self is other or self.uuid == other.uuid

    def root(self) -> Triangle:
        parent = self
        while parent.parent is not None and parent.parent is not parent:
            parent = parent.parent
        return parent

    def do(self, args: Triangle) -> Triangle:
        pass
        return args
