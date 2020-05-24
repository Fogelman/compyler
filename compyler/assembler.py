import llvmlite.ir as ir
import llvmlite.binding as llvm

import unittest
from collections import namedtuple
from ctypes import CFUNCTYPE, c_double
from enum import Enum
from compyler.node import Context

# https://gist.github.com/alendit/defe3d518cd8f3f3e28cb46708d4c9d6


class Assembler(object):
    def __init__(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.env = dict()
        self.module = ir.Module(name=__file__)
        self._headers()
        self._main()
        self.target = llvm.Target.from_default_triple()

    def _main(self):
        # self.module.triple = self.binding.get_default_triple()
        ty = ir.FunctionType(ir.VoidType(), [], False)
        func = ir.Function(self.module, ty, name="main")
        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

    def Evaluate(self, ast, st, optimize=True, llvmdump=False):
        """Evaluate code in ast.

        Returns None for definitions and externs, and the evaluated expression
        value for toplevel expressions.
        """
        # Parse the given code and generate code from it

        context = Context(st, self.builder, self.module, self.env)
        ast.Evaluate(context)
        self.builder.ret_void()

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
            pmb.opt_level = 3
            pm = llvm.create_module_pass_manager()
            pmb.populate(pm)
            pm.run(llvmmod)

            if llvmdump:
                print('======== Optimized LLVM IR')
                print(str(llvmmod))

        # Create a MCJIT execution engine to JIT-compile the module. Note that
        # ee takes ownership of target_machine, so it has to be recreated a new
        # each time we call create_mcjit_compiler.
        target_machine = self.target.create_target_machine()
        with llvm.create_mcjit_compiler(llvmmod, target_machine) as ee:
            ee.finalize_object()

            if llvmdump:
                print('======== Machine code')
                print(target_machine.emit_assembly(llvmmod))

            fptr = CFUNCTYPE(c_double)(ee.get_function_address("main"))
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

    def _headers(self):

        int8 = ir.IntType(8).as_pointer()

        fmt = "%i\n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt

        ty = ir.FunctionType(ir.IntType(32), [int8], var_arg=True)
        printf = ir.Function(self.module, ty, name="printf")

        self.env["ftm"] = global_fmt  # fmt_arg
        self.env["printf"] = printf
