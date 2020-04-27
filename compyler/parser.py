from rply import ParserGenerator
from compyler.node import *


class Parser:

    def __init__(self):
        self.pg = ParserGenerator(['INTEGER', 'BOOLEAN', 'NONE', 'IF', 'ELSE', 'WHILE', 'AND', 'OR', 'NOT', 'RETURN',
                                   'PRINT', 'IDENTIFIER', '//', '==', '!=', '>=', '<=', '<', '=', '~', '>', '[',
                                   ']', '{', '}', '|', '&', '^', ',', 'DOT', 'COMMA', 'PLUS', 'MINUS', 'MUL', 'DIV',
                                   'MOD', 'OPEN', 'CLOSE', 'NEWLINE'],
                                  precedence=[('left', ['AND', 'OR']),
                                              ('left', ['NOT']),
                                              ('left', [
                                                  '<', '>', '==', '>=', '<=', '!=']),
                                              ('left', ["|", "^", "&"]),
                                              ('left', ["PLUS", "MINUS"]),
                                              ('left', ["DIV", "MUL", "MOD"]),
                                              ])

    def build(self):

        @self.pg.production("main : stmtlst")
        def main(p):
            return p[0]

        @self.pg.production('stmtlst : stmt')
        def stmtlist_stmt(p):
            return Commands(None, [p[0]])

        @self.pg.production('stmtlst : stmtlst stmt')
        def stmtlist_stmtlist(p):
            p[0].append(p[1])
            return p[0]

        @self.pg.production('stmt : compound_stmt newline')
        @self.pg.production('stmt : compound_stmt')
        @self.pg.production('stmt : simple_stmt newline')
        @self.pg.production('stmt : simple_stmt')
        def stmt(p):
            return p[0]

        @self.pg.production('suite : { newline stmtlst }')
        def suite(p):
            return p[2]

        @self.pg.production('simple_stmt : expr_stmt')
        def simple_stmt(p):
            return p[0]

        @self.pg.production('compound_stmt : if_stmt')
        @self.pg.production('compound_stmt : print_stmt')
        @self.pg.production('compound_stmt : while_stmt')
        def compound_stmt(p):
            return p[0]

        @self.pg.production('if_stmt : IF OPEN logical CLOSE suite')
        @self.pg.production('if_stmt : IF OPEN logical CLOSE suite ELSE suite')
        def if_stmt(p):

            if(len(p) < 6):
                return If(None, children=[p[2], p[4]])
            else:
                return If(None, children=[p[2], p[4], p[6]])

        @self.pg.production('while_stmt : WHILE OPEN logical CLOSE suite')
        def while_stmt(p):

            if(len(p) < 6):
                return While(None, children=[p[2], p[4]])

        @self.pg.production('print_stmt : PRINT OPEN logical CLOSE')
        def print_stmt(p):

            return Print(None, [p[2]])

        @self.pg.production('expr_stmt : logical')
        @self.pg.production('expr_stmt : IDENTIFIER = logical')
        def expr_stmt(p):
            if (len(p) == 1):
                return p[0]
            else:
                return Assignment(p[0].value, [p[2]])

        @self.pg.production('logical : not OR logical')
        @self.pg.production('logical : not AND logical')
        @self.pg.production('logical : not')
        def logical(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinOp(p[1].value, [p[0], p[2]])

        @self.pg.production('not : NOT not')
        @self.pg.production('not : comparison')
        def logical_not(p):
            if len(p) == 1:
                return p[0]
            else:
                return UnOp(p[0].value, [p[1]])

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

        @self.pg.production('arith : term PLUS arith')
        @self.pg.production('arith : term MINUS arith')
        @self.pg.production('arith : term')
        def arith(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinOp(p[1].value, [p[0], p[2]])

        @self.pg.production('term : factor MUL term')
        @self.pg.production('term : factor DIV term')
        @self.pg.production('term : factor MOD term')
        @self.pg.production('term : factor //  term')
        @self.pg.production('term : factor')
        def term(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinOp(p[1].value, [p[0], p[2]])

        @self.pg.production('factor : atom')
        @self.pg.production('factor : ~ factor')
        @self.pg.production('factor : PLUS factor')
        @self.pg.production('factor : MINUS factor')
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

        @self.pg.production('atom : IDENTIFIER')
        def identifier(p):
            return Identifier(p[0].value)

        @self.pg.production('atom : OPEN logical CLOSE')
        def parenteses(p):
            return p[1]

        @self.pg.production('atom : NONE')
        def none(p):
            return AnyVal(None)

        @self.pg.production("newline : NEWLINE")
        @self.pg.production("newline : NEWLINE newline")
        def newline(p):
            return

        @self.pg.error
        def error_handler(token):
            raise ValueError(
                "Ran into a %s where it wasn't expected" % token.gettokentype())

        return self.pg.build()
