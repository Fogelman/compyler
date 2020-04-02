
from abc import ABC, abstractmethod
# from symboltable import SymbolTable


class Node(ABC):

    def __init__(self, value, children=None):
        self.value = value
        self.children = children
        if children is None:
            self.children = list()

    @abstractmethod
    def Evaluate(self):
        pass


class BinOp(Node):

    def Evaluate(self):
        if self.value == "PLUS":
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == "MINUS":
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == "DIVIDE":
            return self.children[0].Evaluate() // self.children[1].Evaluate()
        elif self.value == "MULTIPLY":
            return self.children[0].Evaluate() * self.children[1].Evaluate()


class UnOp(Node):

    def Evaluate(self):
        if self.value == "PLUS":
            return self.children[0].Evaluate()
        elif self.value == "MINUS":
            return -self.children[0].Evaluate()


class IntVal(Node):

    def Evaluate(self):
        return self.value


class NoOp(Node):

    def Evaluate(self):
        return


class Assignments(Node):

    def Evaluate(self):
        self.children[0] = self.children[1].Evaluate()


class Echo(Node):
    def Evaluate(self):
        print(self.children[0].Evaluate())


class Variable(Node):
    def Evaluate(self):
        pass


class Commands(Node):

    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

    # def addChild(self, child):
    #     self.children.append(child)
