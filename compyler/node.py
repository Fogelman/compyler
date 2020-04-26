
from abc import ABC, abstractmethod
import operator as op
from rply.token import BaseBox, Token


class Node(BaseBox, ABC):

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
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '^': op.xor,
        '/': op.truediv,
        '//': op.floordiv,
        '%': op.mod,
        '&': op.and_,
        '|': op.or_,
        '<': op.lt,
        '>': op.gt,
        '<=': op.le,
        '>=': op.ge,
        '==': op.eq,
        '!=': op.ne,
    }

    def Evaluate(self, st):
        return self.op_map[self.value](self.children[0].Evaluate(st), self.children[1].Evaluate(st))


class UnOp(Node):

    def Evaluate(self, st):

        if self.value == "+":
            return self.children[0].Evaluate(st)
        elif self.value == "-":
            return -self.children[0].Evaluate(st)
        elif self.value == "~":
            return ~self.children[0].Evaluate(st)


class IntVal(Node):

    def Evaluate(self, st):
        return int(self.value)


class BoolVal(Node):

    def Evaluate(self, st):
        return bool(self.value)


class AnyVal(Node):

    def Evaluate(self, st):
        return (self.value)


class NoOp(Node):

    def Evaluate(self, st):
        pass


class Assignment(Node):

    def Evaluate(self, st):
        a = self.children[0].Evaluate(st)
        st.set(self.value, a)


class Echo(Node):
    def Evaluate(self, st):

        result = self.children[0].Evaluate(st)
        if type(result) is bool:
            result = int(result)
        print(result, end="\n")


class If(Node):

    def Evaluate(self, st):
        if(self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st)
        elif len(self.children) > 2:
            self.children[2].Evaluate(st)


class While(Node):

    def Evaluate(self, st):
        while(self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st)


class ReadLine(Node):

    def Evaluate(self, st):
        return input()


class Identifier(Node):

    def Evaluate(self, st):
        return st.get(self.value)


class Commands(Node):

    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)
