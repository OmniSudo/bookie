from __future__ import annotations

import importlib
import os
import uuid as uuid
import types


class Triangle:
    name: str = None
    uuid: uuid
    parent: Triangle = None
    data: map = None
    index: dict = {
        'c': 'c',
        'u': 'u',
        'r': 'r',
        'l': 'l'
    }

    def __get_center_child__(self) -> Triangle:
        return self.__center_child__

    def __set_center_child__(self, value: Triangle):
        self.__center_child__ = value
        value.parent = self

    def __get_top_child__(self) -> Triangle:
        return self.__top_child__

    def __set_top_child__(self, value: Triangle):
        self.__top_child__ = value
        value.parent = self

    def __get_left_child__(self) -> Triangle:
        return self.__left_child__

    def __set_left_child__(self, value: Triangle):
        self.__left_child__ = value
        value.parent = self

    def __get_right_child__(self) -> Triangle:
        return self.__right_child__

    def __set_right_child__(self, value: Triangle):
        self.__right_child__ = value
        value.parent = self

    center_child: Triangle = property(__get_center_child__, __set_center_child__)

    top_child: Triangle = property(__get_top_child__, __set_top_child__)
    left_child: Triangle = property(__get_left_child__, __set_left_child__)
    right_child: Triangle = property(__get_right_child__, __set_right_child__)

    __center_child__: Triangle = None

    __top_child__: Triangle = None
    __left_child__: Triangle = None
    __right_child__: Triangle = None

    def __init__(
            self,
            parent: Triangle = None,
            name: str = '',
            index: map = {
                'c': 'c',
                'u': 'u',
                'r': 'r',
                'l': 'l'
            },
            uuid: uuid = None,
            data: map = None,
    ):
        """
        Constructor method for initializing an instance of the class.

        Parameters:
            parent (Triangle, optional): Parent triangle object. Defaults to None.
            name (str, optional): Name of the instance. Defaults to an empty string.
            data (map, optional): Data associated with the instance. Defaults to None.
            index (map, optional): Mapping of index values. Defaults to {'c': 'c', 'u': 'u', 'r': 'r', 'l': 'l'}.
            uuid (uuid, optional): Unique identifier for the instance. Defaults to None.
        """
        self.uuid = uuid
        self.name = name

        indexes = ['c', 'u', 'r', 'l']
        for i in indexes:
            if i not in index:
                self.index[i] = i
            else:
                self.index[i] = index[i]

        self.parent = parent
        self.data = data

    def __eq__(self, other):
        """
        Check if the current Triangle object is equal to another object.

        :param other: The object to compare with.
        :type other: object
        :return: True if the current Triangle object is equal to the other object, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Triangle): return False

        # TODO: Equality from root triangle equality function
        try:
            pass
        except Exception:
            pass

        return self.uuid == other.uuid

    def root(self) -> Triangle:
        """
        Finds the root of the current Triangle.

        Returns:
            The highest parent of the current Triangle

        Examples:
            parent = Triangle()
            triangle = Triangle(parent)
            root_triangle = triangle.root()
            root_triangle == parent
        """
        if self.parent is None or self.uuid == None or self.parent.__eq__(self):
            return self
        return self.parent.root()

    def get(self, arg: str | list[str]) -> object | None:
        """
        Get the Triangle object based on the given argument.

        Parameters:
            arg (str or list): The argument to determine the Triangle object.

        Returns:
            Triangle: The Triangle following the given path

        Example:
            object.get('/u')  # Returns root's 'up' triangle
            object.get('/u/test?asdf='callmemaybe'/u'
            object.get('/function?var=\'test\',othervar=\'othertest\'')
            object.get(['c', 'r'])  # Returns relative 'c' then 'r'
        """
        if isinstance(arg, str):
            return self.__get_split__(arg)
        elif isinstance(arg, list):
            return self.__get_array__(arg)
        else:
            return None

    def __get_split__(self, path) -> object | None:
        """

        This method is used to split a given path into individual segments based on the '/' delimiter.

        Parameters:
            path (str): The path to be split.

        Returns:
            Triangle | None: A triangle at the given path, can be None

        Example:
            path = '/r'
            split_path = self.__get_split__(path)
            # split_path will be an instance of Triangle at the given path relative to root

        """
        split = str.split(path, '/')
        if path.startswith('/'):
            return self.root().__get_array__(split)
        return self.__get_array__(split)

    def __get_array__(self, split: list[str]) -> object | None:
        """
        Retrieves a Triangle based on the given split parameter.

        Args:
            split (list[str]): The split parameter used to retrieve the array.

        Returns:
            Triangle | None: The retrieved array if successful, or None if unsuccessful.
        """
        if len(split) == 0:
            return self
        if len(split[0]) == 0:
            split = split[1:]

        if split[0].startswith("..") and len(split[0]) == 2:
            return self.parent
        elif split[0].startswith(".") and len(split[0]) == 1:
            return self.get(split[1:])

        if self.data is not None and len(self.data) > 0 and split[0].split('?')[0] in self.data:
            return self.invoke(self.data, split)

        if (split[0] == self.index['c']) or (self.center_child is not None and split[0] == self.center_child.uuid):
            return self.center_child.get(split[1:])
        elif (split[0] == self.index['u']) or (self.top_child is not None and split[0] == self.top_child.uuid):
            return self.top_child.get(split[1:])
        elif (split[0] == self.index['r']) or (self.right_child is not None and split[0] == self.right_child.uuid):
            return self.right_child.get(split[1:])
        elif (split[0] == self.index['l']) or (self.left_child is not None and split[0] == self.left_child.uuid):
            return self.left_child.get(split[1:])
        else:
            return None

    def invoke(self, data, split) -> object | None:
        split = split[0].split('?')
        name = split[0]
        args = split[1] if len(split) > 1 else None

        if name in self.data:
            data = self.data[name]
            if type(data) is Triangle:
                return data.get(split[1:])
            elif isinstance(data, types.FunctionType):
                args = args.split(',')  # i='j'
                kwargs = {}
                i = 0
                while i < len(args):
                    if len(args[i]) == 0:
                        continue
                    var = args[i].split('=')
                    if len(var) != 2:
                        return None
                    if var[1].startswith('\'') or var[1].startswith('\"'):
                        while i < len(args) and not (
                                var[1].endswith(var[1][0]) and not var[1].endswith('\\' + var[1][0])
                        ):
                            var = [var[0], var[1] + ',' + args[i + 1]]
                            i += 1
                        i += 1

                        if not var[1].endswith(var[1][0]):
                            return None

                        var[1] = var[1][1:-1]
                    kwargs[var[0].strip()] = (var[1])  # TODO: root lookup object

                ret = data(**kwargs)  # TODO: Process with mind
                if type(ret) is Triangle:
                    return ret.get(split[1:])
                elif len(split[2:]) == 0:
                    return ret
                else:
                    return None
        else:
            return data if len(split) == 1 else None
