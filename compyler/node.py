
from llvmlite import ir
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
    def Evaluate(self, context):
        pass


class Context(object):
    def __init__(self, st, builder, module):
        self.st = st
        self.builder = builder
        self.module = module

    def declare(self, name):
        """Create an alloca in the entry BB of the current function."""
        builder = ir.IRBuilder()
        builder.position_at_start(self.builder.function.entry_basic_block)
        return builder.alloca(ir.DoubleType(), size=None, name=name)


class UnOp(Node):

    op_map = {
        '+': lambda builder, x: x,
        '-': lambda builder, x: builder.neg(x, "unoptmp"),
        '~': lambda builder, x: builder.not_(x, "unoptmp"),
        'not': lambda builder, x: builder.not_(x, "unoptmp"),

    }

    def Evaluate(self, context):
        return self.op_map[self.value](context.builder, self.children[0].Evaluate(context))


class BinOp(Node):

    op_map = {
        '+': lambda builder, x, y: builder.add(x, y, "optmp"),
        '-': lambda builder, x, y: builder.sub(x, y, "optmp"),
        '*': lambda builder, x, y: builder.mul(x, y, "optmp"),
        '^': lambda builder, x, y: builder.xor(x, y, "optmp"),
        '/': lambda builder, x, y: builder.sdiv(x, y, "optmp"),
        '//': lambda builder, x, y: builder.sdiv(x, y, "optmp"),
        '%': lambda builder, x, y: builder.srem(x, y, "optmp"),
        '&': lambda builder, x, y: builder.and_(x, y, "optmp"),
        '|': lambda builder, x, y: builder.or_(x, y, "optmp"),
        '<': lambda builder, x, y: builder.icmp_signed("<", x, y, "optmp"),
        '>': lambda builder, x, y: builder.icmp_signed(">", x, y, "optmp"),
        '<=': lambda builder, x, y: builder.icmp_signed("<=", x, y, "optmp"),
        '>=': lambda builder, x, y: builder.icmp_signed(">=", x, y, "optmp"),
        '==': lambda builder, x, y: builder.icmp_signed("==", x, y, "optmp"),
        '!=': lambda builder, x, y: builder.icmp_signed("!=", x, y, "optmp"),
        'and': lambda builder, x, y: builder.and_(x, y, "optmp"),

    }

    def Evaluate(self, context):
        return self.op_map[self.value](context.builder, self.children[0].Evaluate(context), self.children[1].Evaluate(context))


class IntVal(Node):

    def Evaluate(self, context):
        int32 = ir.IntType(32)
        return ir.Constant(int32, int(self.value))


class BoolVal(Node):

    def Evaluate(self, context):
        int32 = ir.IntType(32)
        return ir.Constant(int32, int(self.value == "True"))


class AnyVal(Node):

    def Evaluate(self, context):
        return (self.value)


class NoOp(Node):

    def Evaluate(self, context):
        pass


class Assignment(Node):

    def Evaluate(self, context):
        block = context.builder.block
        addr = context.declare(self.value)
        context.builder.position_at_end(block)
        x = self.children[0].Evaluate(context)
        context.builder.store(x, addr)
        context.st.set(self.value, addr)


class Identifier(Node):

    def Evaluate(self, context):

        addr = context.st.get(self.value)
        return context.builder.load(addr, self.value)


class Print(Node):
    def Evaluate(self, context):

        result = self.children[0].Evaluate(context.st)
        if type(result) is bool:
            result = int(result)
        print(result, end="\n")


class If(Node):

    def Evaluate(self, context):
        int32 = ir.IntType(32)
        # int1 = ir.IntType(1)

        condition = self.children[0].Evaluate(context)
        pred = context.builder.icmp_signed(
            '!=', condition, ir.Constant(int32, 0))
        # pred = context.builder.trunc(pred, int1, "comptmp")

        with context.builder.if_else(pred) as (then, otherwise):
            with then:
                self.children[1].Evaluate(context)
            with otherwise:
                self.children[2].Evaluate(context)


class While(Node):

    def Evaluate(self, context):
        while self.children[0].Evaluate(context.st):
            self.children[1].Evaluate(context.st)


class ReadLine(Node):

    def Evaluate(self, context):
        return int(input())


class Commands(Node):

    def Evaluate(self, context):
        for child in self.children:
            child.Evaluate(context)

    def append(self, child):
        self.children.append(child)


class FuncAssignment(Node):
    def Evaluate(self, context):
        context.st.set(self.value,
                       FunctionSymbol(
                           self.children[0],
                           self.children[1]))


class FuncCall(Node):
    def Evaluate(self, parent):
        # Ta errado aqui, precisa ser contexto e não st. Rever depois
        st = SymbolTable(None, parent.st)
        func = parent.st.get(self.value)
        arguments = self.children

        if len(arguments) != len(func.arguments):
            raise Exception(
                'The amount of argument passed does not match function declaration')

        for i in range(len(arguments)):
            evaled = arguments[i].Evaluate(parent)
            st.set(func.arguments[i], evaled)

        return func.suite.Evaluate(st)


class Return(Node):
    def Evaluate(self, context):

        if self.children is None or len(self.children) == 0:
            return context.builder.ret_void()

        return context.builder.ret(self.children[0].Evaluate(context))
