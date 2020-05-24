
class FunctionSymbol():
    def __init__(self, name, arguments, suite):
        self.name = name
        self.arguments = arguments
        self.suite = suite


class SymbolTable:

    def __init__(self, symbols=None, parent=None):
        self.symbols = symbols
        self.parent = parent
        if symbols is None:
            self.symbols = {}

    def setfunc(self, key, value):
        st = self
        while st.parent is not None:
            st = st.parent

        if st.symbols.__contains__(key):
            raise Exception("Function already declared")

    def getfunc(self, key, value):
        st = self
        while st.parent is not None:
            st = st.parent

        if not st.symbols.__contains__(key):
            raise Exception("Function not declared")

    def set(self, key, value):
        self.symbols[key] = value

    def get(self, key):
        return self.symbols[key]
