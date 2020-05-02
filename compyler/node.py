
from abc import ABC, abstractmethod

import operator as op
# from symboltable import SymbolTable


class Node(ABC):

    def __init__(self, value, children=None):
        self.value = value
        self.children = children
        if children is None:
            self.children = list()

    @abstractmethod
    def Evaluate(self, st):
        pass


class BinOp(Node):

    op_map = {
        '+': {"function": op.add, "types": ["INT", "BOOL"], "result": "INT"},
        '-': {"function": op.sub,   "types": ["INT", "BOOL"], "result": "INT"},
        '*': {"function": op.mul,   "types": ["INT", "BOOL"], "result": "INT"},
        '/': {"function": op.floordiv,  "types": ["INT", "BOOL"], "result": "INT"},
        '<': {"function": op.lt,    "types": ["INT", "BOOL"], "result": "BOOL"},
        '>': {"function": op.gt,    "types": ["INT", "BOOL"], "result": "BOOL"},
        '<=': {"function": op.le,   "types": ["INT", "BOOL"], "result": "BOOL"},
        '>=': {"function": op.ge,   "types": ["INT", "BOOL"], "result": "BOOL"},
        '==': {"function": op.eq,   "types": ["INT", "BOOL", "STRING"], "result": "BOOL"},
        'AND': {"function": lambda a, b: a and b, "types": ["INT", "BOOL"], "result": "BOOL"},
        'OR': {"function": lambda a, b: a or b, "types": ["INT", "BOOL"], "result": "BOOL"},
        '.': {"function": lambda a, b: str(a) + str(b),   "types": ["INT", "BOOL", "STRING"], "result": "STRING"},
    }

    def Evaluate(self, st):

        l = self.children[0].Evaluate(st)
        r = self.children[1].Evaluate(st)
        operation = self.op_map[self.value]

        error = False

        error |= self.value == "." and l[1] != "STRING"
        # Verify  operation PHP
        error |= ((l[1] == "STRING" and r[1] != "STRING") or (
            l[1] != "STRING" and r[1] == "STRING")) and self.value != "."
        error |= l[1] not in operation["types"] or r[1] not in operation["types"]
        if error:
            raise Exception("Operation not supported by types")

        result = operation["function"](l[0], r[0])
        if operation["result"] == "BOOL":
            result = int(bool(result))
        return (result, operation["result"])


class UnOp(Node):

    op_map = {
        "+": lambda a: +a,
        "-": lambda a: -a,
        "NOT": lambda a: not a
    }

    def Evaluate(self, st):

        child = self.children[0].Evaluate(st)

        if child[1] not in ["BOOL", "INT"]:
            raise SyntaxError(
                f"Cannot apply operation to variable of type {child[1]}")

        result = self.op_map[self.value](child[0])

        if self.value == "NOT":
            result = int(result)
            return (result, "BOOL")

        return (result, child[1])


class IntVal(Node):

    def Evaluate(self, st):
        return (self.value, "INT")


class NoOp(Node):

    def Evaluate(self, st):
        pass


class Assignment(Node):

    def Evaluate(self, st):
        a = self.children[0].Evaluate(st)
        st.set(self.value, a)


class Echo(Node):
    def Evaluate(self, st):
        result = self.children[0].Evaluate(st)[0]
        print(result, end="\n")


class If(Node):

    def Evaluate(self, st):

        if(self.children[0].Evaluate(st)[0]):
            self.children[1].Evaluate(st)
        elif len(self.children) > 2:
            self.children[2].Evaluate(st)


class While(Node):

    def Evaluate(self, st):
        while(self.children[0].Evaluate(st)[0]):
            self.children[1].Evaluate(st)


class BoolVal(Node):

    def Evaluate(self, st):

        parsed = int(self.value == True)
        return (parsed, "BOOL")


class ReadLine(Node):

    def Evaluate(self, st):
        return (int(input()), "INT")


class Identifier(Node):

    def Evaluate(self, st):
        return st.get(self.value)


class StringVal(Node):
    def Evaluate(self, st):
        return (self.value, "STRING")


class Commands(Node):

    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)
