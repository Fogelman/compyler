from json import dumps


class SymbolTable:
    def __init__(self, symbols=None):
        self.symbols = symbols
        if symbols is None:
            self.symbols = {}

    def set(self, key, value):
        self.symbols[key] = value

    def get(self, key):
        return self.symbols[key]

    def __str__(self):
        return f"{self.symbols}"
