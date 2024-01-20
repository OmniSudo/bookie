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

        path = split[0].split('?', 1)[0]
        tri = self.center_child
        i = 0
        while i < len(path) and tri is not None:
            len_remaining = len(path) - i
            # TODO
            if tri is None:
                break

            if len_remaining == 0:
                return tri.center_child.get(split[1:]) if tri.center_child is not None else None
            elif tri.top_child is None: # and len_remaining > 0
                return None
            else: # tri.top_child is not None and len_remaining > 0
                len_top_child_name = len(tri.top_child.name)
                min_len = min(len_remaining, len_top_child_name)
                text = tri.top_child.name[:min_len]
                path_sample = path[i:min_len]
                if text.startswith(path_sample):
                    if len_remaining == len_top_child_name:
                        return tri.top_child.center_child
                    elif len_remaining > len_top_child_name:
                        i += len_top_child_name
                        tri = tri.top_child
                        continue
                    else: # len_remaining < len_top_child_name
                        return None
                elif text < path_sample:
                    if tri.right_child is not None:
                        tri = tri.right_child
                        continue
                    else:
                        return None
                else: # text > path_sample
                    if tri.left_child is not None:
                        tri = tri.left_child
                        continue
                    else:
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
                    path[i:]
                )
                tri.top_child.center_child = value
                return value
            else:
                top_child_name_len = len(tri.top_child.name)
                min_len = min(len_remaining, top_child_name_len)
                text = tri.top_child.name[:min_len]
                partial_path = path[i:min_len]  # Introduce a variable for path[i:min_len]
                if partial_path.startswith(text):
                    if len_remaining == top_child_name_len:
                        tri = tri.top_child
                        tri.center_child = value
                        return value
                    elif len_remaining < top_child_name_len:
                        new = tri.top_child.name[min_len:]
                        prev = tri.top_child

                        tri.top_child = Triangle(
                            tri,
                            text
                        )
                        tri.center_child = value

                        prev.name = new
                        tri.top_child.top_child = prev

                        tri.left_child = prev.left_child
                        tri.top_child.top_child.left_child = None

                        tri.right_child = prev.right_child
                        tri.top_child.top_child.right_child = None
                        tri.top_child.center_child = value
                        return value
                    else:  # len_remaining > top_child_name_len
                        i += top_child_name_len
                        tri = tri.top_child
                        continue
                elif partial_path > text:
                    if tri.right_child is not None:
                        tri = tri.right_child
                        continue
                    else:
                        tri.right_child = Triangle(
                            tri,
                            path[i:]
                        )
                        tri.right_child.top_child = Triangle(
                            tri.right_child,
                            path[i:]
                        )
                        tri.right_child.top_child.center_child = value
                        return value
                elif partial_path < text:
                    if tri.left_child is not None:
                        tri = tri.left_child
                        continue
                    else:
                        tri.left_child = Triangle(
                            tri,
                            path[i:]
                        )
                        tri.left_child.top_child = Triangle(
                            tri.left_child,
                            path[i:]
                        )
                        tri.left_child.top_child.center_child = value
                        return value

        return None