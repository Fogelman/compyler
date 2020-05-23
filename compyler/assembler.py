import llvmlite.ir as ir
import llvmlite.binding as llvm

import unittest
from collections import namedtuple
from ctypes import CFUNCTYPE, c_double
from enum import Enum
from compyler.node import Context


class Assembler(object):
    def __init__(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        self._config()

        self.module = ir.Module()
        self.builder = None
        self.func_symtab = {}

        self._add_builtins(self.module)
        self.target = llvm.Target.from_default_triple()

    def _config(self):
        self.module = ir.Module(name=__file__)
        tp = ir.FunctionType(ir.VoidType(), [])
        func = ir.Function(self.module, tp, name="main")
        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

    def Evaluate(self, ast, st=None, optimize=True, llvmdump=False):
        """Evaluate code in ast.

        Returns None for definitions and externs, and the evaluated expression
        value for toplevel expressions.
        """
        # Parse the given code and generate code from it
        context = Context(self.builder, self.module, {})
        ast.Evaluate(context)

        if llvmdump:
            print('======== Unoptimized LLVM IR')
            print(str(self.module))

        # If we're evaluating a definition or extern declaration, don't do
        # anything else. If we're evaluating an anonymous wrapper for a toplevel
        # expression, JIT-compile the module and run the function to get its
        # result.
        # if not (isinstance(ast, FunctionAST) and ast.is_anonymous()):
        #     return None

        # Convert LLVM IR into in-memory representation
        llvmmod = llvm.parse_assembly(str(self.module))

        # Optimize the module
        if optimize:
            pmb = llvm.create_pass_manager_builder()
            pmb.opt_level = 2
            pm = llvm.create_module_pass_manager()
            pmb.populate(pm)
            pm.run(llvmmod)

            if llvmdump:
                print('======== Optimized LLVM IR')
                print(str(llvmmod))

        # Create a MCJIT execution engine to JIT-compile the module. Note that
        # ee takes ownership of target_machine, so it has to be recreated anew
        # each time we call create_mcjit_compiler.
        target_machine = self.target.create_target_machine()
        with llvm.create_mcjit_compiler(llvmmod, target_machine) as ee:
            ee.finalize_object()

            if llvmdump:
                print('======== Machine code')
                print(target_machine.emit_assembly(llvmmod))

            fptr = CFUNCTYPE(c_double)(ee.get_function_address(ast.proto.name))
            result = fptr()
            return result

    def compile_to_object_code(self):
        """Compile previously evaluated code into an object file.

        The object file is created for the native target, and its contents are
        returned as a bytes object.
        """
        # We use the small code model here, rather than the default one
        # `jitdefault`.
        #
        # The reason is that only ELF format is supported under the `jitdefault`
        # code model on Windows. However, COFF is commonly used by compilers on
        # Windows.
        #
        # Please refer to https://github.com/numba/llvmlite/issues/181
        # for more information about this issue.
        target_machine = self.target.create_target_machine(codemodel='small')

        # Convert LLVM IR into in-memory representation
        llvmmod = llvm.parse_assembly(str(self.module))
        return target_machine.emit_object(llvmmod)

    def _add_builtins(self, module):
        # The C++ tutorial adds putchard() simply by defining it in the host C++
        # code, which is then accessible to the JIT. It doesn't work as simply
        # for us; but luckily it's very easy to define new "C level" functions
        # for our JITed code to use - just emit them as LLVM IR. This is what
        # this method does.

        # Add the declaration of putchar
        putchar_ty = ir.FunctionType(ir.IntType(32), [ir.IntType(32)])
        putchar = ir.Function(module, putchar_ty, 'putchar')

        # Add putchard
        putchard_ty = ir.FunctionType(ir.DoubleType(), [ir.DoubleType()])
        putchard = ir.Function(module, putchard_ty, 'putchard')
        irbuilder = ir.IRBuilder(putchard.append_basic_block('entry'))
        ival = irbuilder.fptoui(putchard.args[0], ir.IntType(32), 'intcast')
        irbuilder.call(putchar, [ival])
        irbuilder.ret(ir.Constant(ir.DoubleType(), 0))
