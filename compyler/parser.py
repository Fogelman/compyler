from rply import ParserGenerator
from compyler.node import UnOp, BinOp, IntVal, AnyVal, Commands, If, While, Print, Assignment, BoolVal, Identifier, FuncAssignment, FuncCall


class Parser:

    pg = ParserGenerator(['INTEGER', 'BOOLEAN', 'NONE', 'IF', 'ELSE', 'WHILE', 'DEF', 'AND', 'OR', 'NOT', 'RETURN',
                          'PRINT', 'IDENTIFIER', '//', '==', '!=', '>=', '<=', '<', '=', '~', '>',
                          '{', '}', '|', '&', '^', 'COMMA', 'PLUS', 'MINUS', 'MUL', 'DIV',
                          'MOD', 'OPEN', 'CLOSE', 'NEWLINE'],
                         precedence=[('left', ['AND', 'OR']),
                                     ('left', ['NOT']),
                                     ('left', [
                                         '<', '>', '==', '>=', '<=', '!=']),
                                     ('left', ["|", "^", "&"]),
                                     ('left', ["PLUS", "MINUS"]),
                                     ('left', ["DIV", "MUL", "MOD"]),
                                     ])

    @staticmethod
    @pg.production("main : stmtlst")
    @pg.production("main : newline stmtlst")
    def main(p):
        return p[len(p) - 1]

    @staticmethod
    @pg.production('stmtlst : stmt')
    def stmtlist_stmt(p):
        return Commands(None, [p[0]])

    @staticmethod
    @pg.production('stmtlst : stmtlst stmt')
    def stmtlist_stmtlist(p):
        p[0].append(p[1])
        return p[0]

    @staticmethod
    @pg.production('arguments : IDENTIFIER')
    def argument(p):
        return [p[0].value]

    @staticmethod
    @pg.production('arguments : arguments COMMA IDENTIFIER')
    def arguments(p):
        p[0].append(p[2].value)
        return p[0]

    @staticmethod
    @pg.production('testlists : logical')
    def testlists(p):
        return [p[0]]

    @staticmethod
    @pg.production('testlists : testlists COMMA logical')
    def testlist(p):
        p[0].append(p[2])
        return p[0]

    @staticmethod
    @pg.production('stmt : compound_stmt newline')
    @pg.production('stmt : compound_stmt')
    @pg.production('stmt : simple_stmt newline')
    def stmt(p):
        return p[0]

    @staticmethod
    @pg.production('suite : { newline stmtlst }')
    def suite(p):
        return p[2]

    @staticmethod
    @pg.production('simple_stmt : expr_stmt')
    def simple_stmt(p):
        return p[0]

    @staticmethod
    @pg.production('compound_stmt : if_stmt')
    @pg.production('compound_stmt : print_stmt')
    @pg.production('compound_stmt : while_stmt')
    @pg.production('compound_stmt : funcdef')
    def compound_stmt(p):
        return p[0]

    @staticmethod
    @pg.production('if_stmt : IF OPEN logical CLOSE suite')
    @pg.production('if_stmt : IF OPEN logical CLOSE suite ELSE suite')
    def if_stmt(p):

        if(len(p) < 6):
            return If(None, children=[p[2], p[4]])
        else:
            return If(None, children=[p[2], p[4], p[6]])

    @staticmethod
    @pg.production('while_stmt : WHILE OPEN logical CLOSE suite')
    def while_stmt(p):

        if(len(p) < 6):
            return While(None, children=[p[2], p[4]])

    @staticmethod
    @pg.production('funcdef : DEF IDENTIFIER OPEN arguments CLOSE suite')
    def funcdef(p):
        return FuncAssignment(p[1].value, [p[3], p[5]])

    @staticmethod
    @pg.production('print_stmt : PRINT OPEN logical CLOSE')
    def print_stmt(p):

        return Print(None, [p[2]])

    @staticmethod
    @pg.production('expr_stmt : logical')
    @pg.production('expr_stmt : IDENTIFIER = logical')
    def expr_stmt(p):
        if (len(p) == 1):
            return p[0]
        else:
            return Assignment(p[0].value, [p[2]])

    @staticmethod
    @pg.production('logical : not OR logical')
    @pg.production('logical : not AND logical')
    @pg.production('logical : not')
    def logical(p):
        if len(p) == 1:
            return p[0]
        else:
            return BinOp(p[1].value, [p[0], p[2]])

    @staticmethod
    @pg.production('not : NOT not')
    @pg.production('not : comparison')
    def logical_not(p):
        if len(p) == 1:
            return p[0]
        else:
            return UnOp(p[0].value, [p[1]])

    @staticmethod
    @pg.production('comparison : bitwise')
    @pg.production('comparison : bitwise < comparison')
    @pg.production('comparison : bitwise > comparison')
    @pg.production('comparison : bitwise == comparison')
    @pg.production('comparison : bitwise != comparison')
    @pg.production('comparison : bitwise >= comparison')
    @pg.production('comparison : bitwise <= comparison')
    def comparison(p):
        if len(p) == 1:
            return p[0]
        else:
            return BinOp(p[1].value, [p[0], p[2]])

    @staticmethod
    @pg.production('bitwise : arith')
    @pg.production('bitwise : arith ^ bitwise')
    @pg.production('bitwise : arith | bitwise')
    @pg.production('bitwise : arith & bitwise')
    def bitwise(p):
        if len(p) == 1:
            return p[0]
        else:
            return BinOp(p[1].value, [p[0], p[2]])

    @staticmethod
    @pg.production('arith : term PLUS arith')
    @pg.production('arith : term MINUS arith')
    @pg.production('arith : term')
    def arith(p):
        if len(p) == 1:
            return p[0]
        else:
            return BinOp(p[1].value, [p[0], p[2]])

    @staticmethod
    @pg.production('term : factor MUL term')
    @pg.production('term : factor DIV term')
    @pg.production('term : factor MOD term')
    @pg.production('term : factor //  term')
    @pg.production('term : factor')
    def term(p):
        if len(p) == 1:
            return p[0]
        else:
            return BinOp(p[1].value, [p[0], p[2]])

    @staticmethod
    @pg.production('factor : atom')
    @pg.production('factor : ~ factor')
    @pg.production('factor : PLUS factor')
    @pg.production('factor : MINUS factor')
    def factor(p):
        if len(p) == 2:
            return UnOp(p[0].value, [p[1]])
        else:
            return p[0]

    @staticmethod
    @pg.production('atom : INTEGER')
    def number(p):
        return IntVal(p[0].value)

    @staticmethod
    @pg.production('atom : BOOLEAN')
    def boolean(p):
        return BoolVal(p[0].value)

    @staticmethod
    @pg.production('atom : IDENTIFIER')
    def identifier(p):
        return Identifier(p[0].value)

    @staticmethod
    @pg.production('atom : OPEN logical CLOSE')
    def parenteses(p):
        return p[1]

    @staticmethod
    @pg.production('atom : NONE')
    def none(p):
        return AnyVal(None)

    @staticmethod
    @pg.production('atom : IDENTIFIER OPEN testlists CLOSE')
    def funcall(p):
        return FuncCall(p[0].value, p[2])

    @staticmethod
    @pg.production("newline : NEWLINE")
    @pg.production("newline : NEWLINE newline")
    def newline(p):
        return

    @staticmethod
    @pg.error
    def error_handler(token):
        raise ValueError(
            "Ran into a %s where it wasn't expected" % token.gettokentype())

    def build(self):
        return self.pg.build()
