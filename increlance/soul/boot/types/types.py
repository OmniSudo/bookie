from increlance.triangle import Triangle


class Types(Triangle):
    def __init__(self, boot: Triangle):
        super().__init__(
            boot,
            self.__class__.__name__
        )

    def register(self, type: type) -> None:
        print(f"Registering type: '{type.__name__}'")
        self.data[type.__name__] = type

    def unregister(self, type: type) -> None:
        self.data.pop(type.__name__, None)

    def unregister_all(self) -> None:
        self.data.clear()

    def find(self, type: str, package: str = None) -> type:
        try:
            if package is not None:
                module = self.root().get("/Soul/Bootloader/Importer/include")(package, package)
                type = module.getattr(type)
            else:
                type = self.data[type] if type in self.data else None

            return type
        except Exception as e:
            # TODO: Failed to find the type
            return None

    def new(self, type: str, package: str = None, **kwargs) -> object:
        try:
            type = self.find(type, package)
            return type(**kwargs)
        except Exception as e:
            # TODO: Failed to instantiate type
            print(f"Could not instantiate type: '{type}'")
            return None
