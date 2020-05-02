
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
        '+': {"function": op.add, "types": ["INT", "BOOL"]},
        '-': {"function": op.sub,   "types": ["INT", "BOOL"]},
        '*': {"function": op.mul,   "types": ["INT", "BOOL"]},
        '^': {"function": op.xor,   "types": ["INT", "BOOL"]},
        '/': {"function": op.floordiv,  "types": ["INT", "BOOL"]},
        '%': {"function": op.mod,   "types": ["INT", "BOOL"]},
        '&': {"function": op.and_,  "types": ["INT", "BOOL"]},
        '|': {"function": op.or_,   "types": ["INT", "BOOL"]},
        '<': {"function": op.lt,    "types": ["INT", "BOOL"]},
        '>': {"function": op.gt,    "types": ["INT", "BOOL"]},
        '<=': {"function": op.le,   "types": ["INT", "BOOL"]},
        '>=': {"function": op.ge,   "types": ["INT", "BOOL"]},
        '==': {"function": op.eq,   "types": ["INT", "BOOL", "STRING"]},
        '!=': {"function": op.ne,   "types": ["INT", "BOOL", "STRING"]},
        '.': {"function": lambda a, b: str(a) + str(b),   "types": ["INT", "BOOL", "STRING"]},
        'AND': {"function": lambda a, b: a and b, "types": ["INT", "BOOL"]},
        'OR': {"function": lambda a, b: a or b, "types": ["INT", "BOOL"]},
    }

    def Evaluate(self, st):

        l = self.children[0].Evaluate(st)
        r = self.children[1].Evaluate(st)
        operation = self.op_map[self.value]

        error = False

        error |= self.value == "." and l[1] != "STRING"
        error |= (l[1] == "STRING" or r[1] == "STRING") and self.value != "."
        error |= l[1] not in operation["types"] or r[1] not in operation["types"]

        if error:
            raise Exception("Operation not supported by types")
        return (operation["function"](l[0], r[0]), "INT")


class UnOp(Node):

    op_map = {
        "+": lambda a: +a,
        "-": lambda a: -a,
        "NOT": lambda a: not a
    }

    def Evaluate(self, st):

        result = self.children[0].Evaluate(st)

        if result[1] not in ["BOOL", "INT"]:
            raise SyntaxError(
                f"Cannot apply operation to variable of type {result[1]}")
        return (self.op_map[self.value](result[0]), result[1])


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
        if type(result) is bool:
            result = int(result)
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
