from json import dumps


class FunctionSymbol():
    def __init__(self, arguments, suite):
        self.arguments = arguments
        self.suite = suite


class SymbolTable:
    def __init__(self, symbols=None, parent=None):
        self.symbols = symbols
        self.parent = parent

        if symbols is None:
            self.symbols = {}

    def set(self, key, value):
        self.symbols[key] = value

    def get(self, key):

        if self.symbols.__contains__(key):
            return self.symbols[key]
        elif self.parent:
            return self.parent.symbols[key]

        raise Exception(f"{key} not defined")

    def contains(self, key):
        if self.symbols.__contains__(key):
            return self.symbols[key]
        elif self.parent:
            return self.parent.contains(key)

        return False

    def __str__(self):
        return f"{self.symbols}"
