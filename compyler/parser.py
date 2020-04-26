from rply import ParserGenerator
from compyler.node import *


class Parser:

    def __init__(self):
        self.pg = ParserGenerator(['INTEGER', 'BOOLEAN', 'IF', 'ELSE', 'NONE', 'AND', 'OR', 'NOT', 'IDENTIFIER', '==', '!=', '>=', '<=', '<', '~', '!',
                                   '^', '=', '>', '[', ']', '{', '}', '|', ',', '&', 'DOT', 'COLON', 'PLUS', 'MINUS', 'MUL', 'DIV', '//', 'MOD', 'OPEN', 'CLOSE', 'NEWLINE'],
                                  precedence=[('left', ['<', '>', '==', '>=', '<=', '!=']),
                                              ('left', ["|"]),
                                              ('left', ["^"]),
                                              ('left', ["&"]),
                                              ('left', ["PLUS", "MINUS"]),
                                              ('left', ["DIV", "MUL", "MOD"])])

    def build(self):

        @self.pg.production('comparison : bitwise')
        @self.pg.production('comparison : bitwise < comparison')
        @self.pg.production('comparison : bitwise > comparison')
        @self.pg.production('comparison : bitwise == comparison')
        @self.pg.production('comparison : bitwise != comparison')
        @self.pg.production('comparison : bitwise >= comparison')
        @self.pg.production('comparison : bitwise <= comparison')
        def comparison(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinOp(p[1].value, [p[0], p[2]])

        @self.pg.production('bitwise : arith')
        @self.pg.production('bitwise : arith ^ bitwise')
        @self.pg.production('bitwise : arith | bitwise')
        @self.pg.production('bitwise : arith & bitwise')
        def bitwise(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinOp(p[1].value, [p[0], p[2]])

        @self.pg.production('arith : term')
        @self.pg.production('arith : term PLUS arith')
        @self.pg.production('arith : term MINUS arith')
        def arith(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinOp(p[1].value, [p[0], p[2]])

        @self.pg.production('term : factor')
        @self.pg.production('term : factor MUL term')
        @self.pg.production('term : factor DIV term')
        @self.pg.production('term : factor MOD term')
        @self.pg.production('term : factor //  term')
        def term(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinOp(p[1].value, [p[0], p[2]])

        @self.pg.production('factor : atom')
        @self.pg.production('factor : PLUS factor')
        @self.pg.production('factor : MINUS factor')
        @self.pg.production('factor : ~ factor')
        def factor(p):
            if len(p) == 2:
                return UnOp(p[0].value, [p[1]])
            else:
                return p[0]

        @self.pg.production('atom : INTEGER')
        def number(p):
            return IntVal(p[0].value)

        @self.pg.production('atom : BOOLEAN')
        def boolean(p):
            return BoolVal(p[0].value)

        @self.pg.production('atom : OPEN INTEGER CLOSE')
        def parenteses(p):
            return IntVal(p[1].value)

        @self.pg.production('atom : NONE')
        def none(p):
            return AnyVal(None)

        return self.pg.build()
