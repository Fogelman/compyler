from rply import ParserGenerator
from compyler.node import *


class Parser:

    def __init__(self):
        self.pg = ParserGenerator(['INTEGER', 'BOOLEAN', 'IF', 'ELSE', 'AND', 'OR', 'NOT', 'IDENTIFIER', '==', '!=', '>=', '<=', '<',
                                   '=', '>', '[', ']', '{', '}', '|', ',', 'DOT', 'COLON', 'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'OPEN', 'CLOSE', 'NEWLINE'],
                                  precedence=[('left', ["PLUS", "MINUS"]),
                                              ('left', ["DIV", "MUL", "MOD"])])

    def build(self):
        @self.pg.production('main : INTEGER')
        def main(p):
            return Echo(None, [IntVal(p[0])])

        return self.pg.build()
