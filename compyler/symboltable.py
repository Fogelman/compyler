

class SymbolTable:
    def __init__(self, symbols=None, offset=0):
        self.offset = offset
        self.symbols = symbols

        self.dsize = {
            "INT": 4,
            "BOOL": 4
        }
        if symbols is None:
            self.symbols = {}

    def set(self, key, value):

        if self.symbols.__contains__(key):
            return self.symbols[key], False

        self.offset += self.dsize[value]
        self.symbols[key] = [value, self.offset]
        return self.symbols[key], True

    def get(self, key):
        return self.symbols[key]
