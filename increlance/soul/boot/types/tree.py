from increlance.triangle import Triangle


class Tree(Triangle):
    def __init__(self, parent: Triangle, name: str):
        super().__init__(
            parent,
            name
        )
        self.center_child = Triangle(
            self,
            ''
        )

    def __get_array__(self, split: list[str]) -> object | None:
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
        tri = self.center_child
        i = 0
        while i < len(var) and tri is not None:
            lenvar = len(var) - i
            if tri.top_child is not None:
                skip = len(tri.top_child.name)
                if tri.top_child.name == var[i:skip if skip < lenvar else lenvar]:
                    if lenvar > skip:
                        tri = tri.top_child
                        i += skip
                    elif lenvar == skip:
                        tri = tri.center_child
                        return tri.center_child.get(split[1:]) if tri.center_child is not None else None
                elif tri.right_child is not None:
                    if tri.top_child.name < var[i:skip]:
                        tri = tri.right_child
                elif tri.left_child is not None:
                    if tri.top_child.name > var[i:skip]:
                        tri = tri.left_child
                else:
                    # Invalid path
                    return None
            else:
                # Invalid path
                return None

        if tri is not None:
            return tri.get(split[1:])
        return None

    def set(self, path: str, value: Triangle) -> Triangle:
        tri = self.center_child
        i = 0
        len_path = len(path)
        while i < len_path:
            len_remaining = len_path - i
            if tri.top_child is None:
                tri.top_child = Triangle(
                    tri,
                    path[i:len_remaining]
                )
                tri.center_child = value
                return value
            else:
                top_child_name_len = len(tri.top_child.name)
                min_len = min(len_remaining, top_child_name_len)
                text = tri.top_child.name[:min_len]
                if path[i:min_len].startswith(text):
                    if len_remaining == top_child_name_len:
                        tri = tri.top_child
                        tri.center_child = value
                        return value
                    elif len_remaining < top_child_name_len:
                        new = tri.top_child.name[min_len + 1:]
                        prev = tri.top_child
                        tri.top_child = Triangle(
                            tri,
                            text
                        )
                        tri.center_child = value
                        tri.top_child = prev

                        tri.left_child = prev.left_child
                        tri.top_child.left_child = None

                        tri.right_child = prev.right_child
                        tri.top_child.right_child = None
                        tri.top_child.name = new

                        tri.top_child.center_child = value
                        return value
                    else:  # len_remaining > top_child_name_len
                        pass
                        i += min_len
                        # TODO: Finish
                if False:
                    pass


        return None
