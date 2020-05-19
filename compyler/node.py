
from abc import ABC, abstractmethod

import operator as op


class Node(ABC):
    id = -1

    def __init__(self, value, children=None):
        self.id = Node.new()
        self.value = value
        self.children = children
        if children is None:
            self.children = list()

    @staticmethod
    def new():
        Node.id += 1
        return Node.id

    @abstractmethod
    def Evaluate(self, st):
        pass


class NoOp(Node):

    def Evaluate(self, st):
        pass


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


class BinOp(Node):

    op_map = {
        '+': {"function": "ADD EAX, EBX;\nMOV EBX, EAX\n", "types": ["INT", "BOOL"], "result": "INT"},
        '-': {"function": "SUB EAX, EBX;\nMOV EBX, EAX\n",   "types": ["INT", "BOOL"], "result": "INT"},
        '*': {"function": "IMUL EBX;\nMOV EBX, EAX;\n",   "types": ["INT", "BOOL"], "result": "INT"},
        '/': {"function": "IDIV EBX;\nMOV EBX, EAX;\n",  "types": ["INT", "BOOL"], "result": "INT"},
        '<': {"function": "CMP EAX, EBX;\nCALL binop_jl;\n",    "types": ["INT", "BOOL"], "result": "BOOL"},
        '>': {"function": "CMP EAX, EBX;\nCALL binop_jg;\n",    "types": ["INT", "BOOL"], "result": "BOOL"},
        '<=': {"function": "CMP EAX, EBX;\nCALL binop_jle;\n",   "types": ["INT", "BOOL"], "result": "BOOL"},
        '>=': {"function": "CMP EAX, EBX;\nCALL binop_jge;\n",   "types": ["INT", "BOOL"], "result": "BOOL"},
        '==': {"function": "CMP EAX, EBX;\nCALL binop_je;\n",   "types": ["INT", "BOOL", "STRING"], "result": "BOOL"},
        'AND': {"function": "AND EAX, EBX;\nMOV EBX, EAX\n", "types": ["INT", "BOOL"], "result": "BOOL"},
        'OR': {"function": "OR EAX, EBX;\nMOV EBX, EAX\n", "types": ["INT", "BOOL"], "result": "BOOL"},
    }

    def Evaluate(self, st):

        l = self.children[0].Evaluate(st)
        r = self.children[1].Evaluate(st)
        operation = self.op_map[self.value]

        error = False

        result = l[0]
        result += "PUSH EBX ; empilha f\n"
        result += r[0]
        result += "POP EAX ;\n"
        result += operation["function"]

        # error |= ((l[1] == "STRING" and r[1] != "STRING") or (
        #     l[1] != "STRING" and r[1] == "STRING")) and self.value != "."
        error |= l[1] not in operation["types"] or r[1] not in operation["types"]
        if error:
            raise Exception(f"Type {l[1]} and {r[1]} cannot be operated")

        # result = operation["function"](l[0], r[0])

        return (result, operation["result"])


class Echo(Node):
    def Evaluate(self, st):

        r = self.children[0].Evaluate(st)[0]
        r += """PUSH EBX; Empilhe os argumentos
CALL print; Chamada da função
POP EBX; Desempilhe os argumentos\n"""

        return (r, None)


class ReadLine(Node):

    def Evaluate(self, st):
        return (f"MOV EBX, ${0};\n", "BOOL")


class If(Node):

    def Evaluate(self, st):

        r = self.children[0].Evaluate(st)[0]
        r += f"""CMP EBX, False ; verifica se o teste deu falso
JE IF_{self.id} ; vai para o if
{self.children[1].Evaluate(st)[0]}
JMP IF_EXIT_{self.id}
IF_{self.id}:
{self.children[2].Evaluate(st)[0]}
IF_EXIT_{self.id}:\n\n"""
        return (r, None)


class While(Node):

    def Evaluate(self, st):
        return (f"""LOOP_{self.id}: ; o unique identifier do nó while é 34
; instruções do filho esquerdo do while - retorna o resultado em EBX
{self.children[0].Evaluate(st)[0]}
CMP EBX, False ; verifica se o teste deu falso
JE EXIT_{self.id} ; e sai caso for igual a falso.
{self.children[1].Evaluate(st)[0]}
; instruções do filho direito do while.
JMP LOOP_{self.id} ; volta para testar de novo
EXIT_{self.id}:\n\n""", None)


class Assignment(Node):

    def Evaluate(self, st):

        r = "PUSH DWORD 0;\n"
        c = self.children[0].Evaluate(st)
        offset = st.set(self.value, c[1])
        r += c[0]
        r += f"MOV [EBP-{offset[1]}], EBX;\n"

        return (r, c[1])


class Identifier(Node):

    def Evaluate(self, st):
        get = st.get(self.value)
        offset = get[1]
        r = f"""MOV EBX, [EBP-{offset}];\n"""
        return (r, get[0])


class IntVal(Node):

    def Evaluate(self, st):
        return (f"MOV EBX, ${self.value};\n", "BOOL")


class StringVal(Node):
    def Evaluate(self, st):
        return (f"MOV EBX, ${0};\n", "BOOL")


class BoolVal(Node):

    def Evaluate(self, st):
        parsed = int(self.value == True)
        return (f"MOV EBX, ${parsed};\n", "BOOL")


class Commands(Node):
    def Evaluate(self, st):

        r = ""
        for child in self.children:
            r += child.Evaluate(st)[0]

        return (r, None)
