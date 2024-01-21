from __future__ import annotations

from inspect import signature
import uuid as id
import types


class Triangle:
    name: str = None
    data: dict = {}
    index: dict = {
        'c': 'c',
        'u': 'u',
        'r': 'r',
        'l': 'l'
    }

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
        self.__center_child__ = value
        if value is not None:
            value.parent = self

    def __get_top_child__(self) -> Triangle:
        return self.__top_child__

    def __set_top_child__(self, value: Triangle):
        self.__top_child__ = value
        if value is not None:
            value.parent = self

    def __get_left_child__(self) -> Triangle:
        return self.__left_child__

    def __set_left_child__(self, value: Triangle):
        self.__left_child__ = value
        if value is not None:
            value.parent = self

    def __get_right_child__(self) -> Triangle:
        return self.__right_child__

    def __set_right_child__(self, value: Triangle):
        self.__right_child__ = value
        if value is not None:
            value.parent = self

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
            index: map = {
                'c': 'c',
                'u': 'u',
                'r': 'r',
                'l': 'l'
            },
            uuid: bool | id.UUID = False,
            data: dict = None,
    ):
        """
        Constructor method for initializing an instance of the class.

        Parameters:
            parent (Triangle, optional): Parent triangle object. Defaults to None.
            name (str, optional): Name of the instance. Defaults to an empty string.
            data (dict, optional): Data associated with the instance. Defaults to None.
            index (dict, optional): Mapping of index values. Defaults to {'c': 'c', 'u': 'u', 'r': 'r', 'l': 'l'}.
            uuid (bool, uuid, optional): Unique identifier for the instance. Defaults to False to imply a unique identifier will not be generated.
        """
        self.parent = parent
        self.name = name

        if data is None:
            data = dict()
        if data is None:
            data = {}

        if isinstance(uuid, id.UUID):
            self.__uuid__ = uuid
        elif uuid:
            get = self.get( "/Soul/Bootloader/Database/tables/triangle/get_id")
            if get is not None:
                self.__uuid__ = get(self)
            else:
                self.uuid = id.uuid4()

        indexes = ['c', 'u', 'r', 'l']
        for i in indexes:
            if i not in index:
                self.index[i] = i
            else:
                self.index[i] = index[i]

        self.data = data if data is not None else self.data

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

        return self is other or self.uuid == other.uuid

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
        parent = self
        while parent.parent is not None and parent.parent is not parent:
            parent = parent.parent
        return parent

    def get(self, arg: str | list[str]) -> Triangle | types.FunctionType | object | None:
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
            # TODO: Log that no method for getting passed path exists
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
            return self.__get_array__(split)

        if split[0].startswith("..") and len(split[0]) == 2:
            return self.parent.get(split[1:]) if self.parent is not None else None
        elif split[0].startswith(".") and len(split[0]) == 1:
            return self.get(split[1:])

        var = split[0].split('?', 1)[0]
        if hasattr(self, var):
            return self.invoke(getattr(self, var), split)
        if self.data is not None and len(self.data) > 0 and var in self.data:
            return self.invoke(self.data[var], split[1:])

        if (split[0] == self.index['c']) or (self.center_child is not None and (
                split[0] == self.center_child.uuid or split[0] == self.center_child.name)):
            return self.center_child.get(split[1:])
        elif (split[0] == self.index['u']) or (
                self.top_child is not None and (split[0] == self.top_child.uuid or split[0] == self.top_child.name)):
            return self.top_child.get(split[1:])
        elif (split[0] == self.index['r']) or (self.right_child is not None and (
                split[0] == self.right_child.uuid or split[0] == self.right_child.name)):
            return self.right_child.get(split[1:])
        elif (split[0] == self.index['l']) or (
                self.left_child is not None and (split[0] == self.left_child.uuid or split[0] == self.left_child.name)):
            return self.left_child.get(split[1:])
        else:
            # TODO: Log that no matching path could be found
            return None

    def invoke(self, data, split) -> object | None:
        split = split[0].split('?', 1)
        name = split[0]
        args = split[1] if len(split) > 1 else None

        if isinstance(data, Triangle):
            return data.__get_array__(split)

        if isinstance(data, types.FunctionType) or isinstance(data, types.MethodType):
            kwargs = {}

            if args is not None and len(args) > 0:
                args = args.split('&')  # i='j'
                i = 0
                while i < len(args):
                    if len(args[i]) == 0:
                        continue
                    var = args[i].split('=', 1)
                    if len(var) != 2:
                        # TODO: Log that arg does not have a value
                        return None
                    if var[1].startswith('\'') or var[1].startswith('\"'):
                        while i < len(args) and not (
                                var[1].endswith(var[1][0]) and not var[1].endswith('\\' + var[1][0])
                        ):
                            var = [var[0], var[1] + '&' + args[i + 1]]
                            i += 1

                        if not var[1].endswith(var[1][0]):
                            # TODO: Log that string does not have a terminating ' or "
                            return None

                        var[1] = var[1][1:-1]
                    i += 1
                    kwargs[var[0].strip()] = (var[1])  # TODO: root lookup object

            ret = None
            try:
                argc = len(signature(data).parameters)
                if argc == 0 and len(kwargs) == 0:
                    ret = data()
                elif argc != 0 and len(kwargs) == 0:
                    return data
                else:
                    ret = data(**kwargs)
            except Exception as e:
                print(f"Failed to invoke {name}:", e)
            if type(ret) is Triangle:
                return ret.get(split[1:])
            elif len(split[2:]) == 0:
                return ret
            else:
                try:
                    return self.invoke(ret, split[1:])
                except Exception as e:
                    # TODO: Log that recursive call into triangle failed
                    return None
        else:
            if len(split) == 1:
                return data
            elif isinstance(data, Triangle):
                return data.get(split[1:])

        # TODO: Log that no behaviour is defined for a datum of type T
        return None

    def save(self) -> bool:
        save = self.get('/Soul/Bootloader/Database/tables/triangle/save')
        if save is not None:
            save(self)
            return True
        return False

    def load(self) -> bool:
        load = self.get('Soul/Bootloader/Database/tables/triangle/load')
        if load is not None:
            load(self)
            return True
        return False
