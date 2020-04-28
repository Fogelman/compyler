
from rply.token import BaseBox
from abc import ABC, abstractmethod
import operator as op
from compyler.symboltable import FunctionSymbol, SymbolTable


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
        'and': lambda a, b: a and b,

    }

    def Evaluate(self, st):
        return self.op_map[self.value](self.children[0].Evaluate(st), self.children[1].Evaluate(st))


class UnOp(Node):

    op_map = {
        '+': lambda a: +a,
        '-': lambda a: -a,
        '~': lambda a: ~a,
        'not': lambda a: not a,

    }

    def Evaluate(self, st):
        return self.op_map[self.value](self.children[0].Evaluate(st))


class IntVal(Node):

    def Evaluate(self, st):
        return int(self.value)


class BoolVal(Node):

    def Evaluate(self, st):
        return self.value == "True"


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


class Print(Node):
    def Evaluate(self, st):

        result = self.children[0].Evaluate(st)
        if type(result) is bool:
            result = int(result)
        print(result, end="\n")


class If(Node):

    def Evaluate(self, st):
        if self.children[0].Evaluate(st):
            self.children[1].Evaluate(st)
        elif len(self.children) > 2:
            self.children[2].Evaluate(st)


class While(Node):

    def Evaluate(self, st):
        while self.children[0].Evaluate(st):
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

    def append(self, child):
        self.children.append(child)


class FuncAssignment(Node):
    def Evaluate(self, st):
        st.set(self.value,
               FunctionSymbol(
                   self.children[0],
                   self.children[1]))


class FuncCall(Node):
    def Evaluate(self, st_parent):

        st = SymbolTable(None, st_parent)
        func = st_parent.get(self.value)
        arguments = self.children

        if len(arguments) != len(func.arguments):
            raise Exception(
                'The amount of argument passed does not match function declaration')

        for i in range(len(arguments)):
            evaled = arguments[i].Evaluate(st_parent)
            st.set(func.arguments[i], evaled)

        return func.suite.Evaluate(st)
