
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
    def __init__(self, st, builder, module, env=dict()):
        self.st = st
        self.builder = builder
        self.module = module
        self.env = env

    def new(self):
        st = SymbolTable(parent=self.st)
        builder = self.builder
        module = self.module
        env = self.env
        return Context(st, builder, module, env)

    def declare(self, name):
        """Create an alloca in the entry BB of the current function."""
        int32 = ir.IntType(32)
        return self.builder.alloca(int32, name=name)


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
        addr = context.st.contains(self.value)
        if not addr:
            addr = context.declare(self.value)

        x = self.children[0].Evaluate(context)
        context.builder.store(x, addr)
        context.st.set(self.value, addr)


class Identifier(Node):

    def Evaluate(self, context):

        addr = context.st.get(self.value)
        return context.builder.load(addr)


class Print(Node):
    def Evaluate(self, context):
        int8 = ir.IntType(8).as_pointer()

        printf = context.env["printf"]
        ftm = context.env["ftm"]
        arg = context.builder.bitcast(ftm, int8)
        result = self.children[0].Evaluate(context)
        context.builder.call(printf, [arg, result])


class If(Node):

    def Evaluate(self, context):
        int32 = ir.IntType(32)

        condition = self.children[0].Evaluate(context)
        pred = context.builder.icmp_signed(
            '!=', condition, ir.Constant(int32, 0))

        with context.builder.if_else(pred) as (then, otherwise):
            with then:
                self.children[1].Evaluate(context)

            with otherwise:
                if len(self.children) > 2:
                    self.children[2].Evaluate(context)


class While(Node):

    def Evaluate(self, context):
        int32 = ir.IntType(32)
        loop = context.builder.function.append_basic_block('loop')
        context.builder.branch(loop)
        context.builder.position_at_start(loop)
        self.children[1].Evaluate(context)
        endcond = self.children[0].Evaluate(context)
        cmp = context.builder.icmp_signed(
            '!=', endcond, ir.Constant(int32, 0),
            'loopcond')

        after = context.builder.function.append_basic_block('afterloop')
        context.builder.cbranch(cmp, loop, after)
        context.builder.position_at_start(after)


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

    def _create(self, context):
        int32 = ir.IntType(32)
        args, _ = self.children
        ty = ir.FunctionType(int32, [int32 for i in range(len(args))])
        if self.value in context.module.globals:

            existing_func = context.module[self.value]
            if not isinstance(existing_func, ir.Function):
                raise Exception('Function/Global name collision', self.value)
            if not existing_func.is_declaration():
                raise Exception('Redifinition of {0}'.format(self.value))
            if len(existing_func.function_type.args) != len(ty.args):
                raise Exception(
                    'Redifinition with different number of arguments')
            func = context.module.globals[self.value]
        else:
            # Otherwise create a new function
            func = ir.Function(context.module, ty, self.value)
        return func

    def Evaluate(self, parent):

        args, body = self.children
        context = parent.new()
        func = self._create(context)
        block = func.append_basic_block('entry')
        context.builder = ir.IRBuilder(block)

        for i, arg in enumerate(func.args):
            arg.name = args[i]
            addr = context.declare(arg.name)
            context.builder.store(arg, addr)
            context.st.set(arg.name, addr)

        body.Evaluate(context)
        return func


class FuncCall(Node):
    def Evaluate(self, context):

        arguments = self.children
        func = context.module.get_global(self.value)
        if func is None or not isinstance(func, ir.Function):
            raise Exception('Call to unknown function', self.value)
        if len(func.args) != len(arguments):
            raise Exception('Call argument length mismatch', self.value)

        call_args = [argument.Evaluate(context) for argument in arguments]
        return context.builder.call(func, call_args, 'calltmp')


class Return(Node):
    def Evaluate(self, context):

        if self.children is None or len(self.children) == 0:
            return context.builder.ret_void()

        return context.builder.ret(self.children[0].Evaluate(context))
