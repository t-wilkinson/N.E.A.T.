class Default(dict):
    def __init__(self, default):
        super().__init__()
        self.default = default

    def __iter__(self):
        return iter(self.values())

    def __missing__(self, key):
        self[key] = result = []
        return result

    def __getitem__(self, key):
        if isinstance(key, slice):
            return list(self.values())[key]
        elif key not in self:
            return self.__missing__(key)
        elif isinstance(key, int):
            return super().__getitem__(key)


d = Default(list)
