
from abc import ABC, abstractmethod
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

    def Evaluate(self, st):
        if self.value == "PLUS":
            return self.children[0].Evaluate(st) + self.children[1].Evaluate(st)
        elif self.value == "MINUS":
            return self.children[0].Evaluate(st) - self.children[1].Evaluate(st)
        elif self.value == "DIVIDE":
            return self.children[0].Evaluate(st) // self.children[1].Evaluate(st)
        elif self.value == "MULTIPLY":
            return self.children[0].Evaluate(st) * self.children[1].Evaluate(st)
        elif self.value == "AND":
            return self.children[0].Evaluate(st) and self.children[1].Evaluate(st)
        elif self.value == "OR":
            return self.children[0].Evaluate(st) or self.children[1].Evaluate(st)
        elif self.value == "LESS":
            return self.children[0].Evaluate(st) < self.children[1].Evaluate(st)
        elif self.value == "GREATER":
            return self.children[0].Evaluate(st) > self.children[1].Evaluate(st)
        elif self.value == "EQUAL":
            return self.children[0].Evaluate(st) == self.children[1].Evaluate(st)


class UnOp(Node):

    def Evaluate(self, st):
        if self.value == "PLUS":
            return self.children[0].Evaluate(st)
        elif self.value == "MINUS":
            return -self.children[0].Evaluate(st)
        elif self.value == "NOT":
            return not self.children[0].Evaluate(st)


class IntVal(Node):

    def Evaluate(self, st):
        return self.value


class NoOp(Node):

    def Evaluate(self, st):
        pass


class Assignment(Node):

    def Evaluate(self, st):
        a = self.children[0].Evaluate(st)
        st.set(self.value, a)


class Echo(Node):
    def Evaluate(self, st):
        print(self.children[0].Evaluate(st), end="\n")


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
