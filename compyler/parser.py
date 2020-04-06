from compyler.tokenizer import Tokenizer
from compyler.node import BinOp, UnOp, IntVal, NoOp, Identifier, Assignment, Commands, Echo, NoOp


class Parser:
    tokens = None

    @staticmethod
    def parseBlock():
        tokens = Parser.tokens
        result = []
        if tokens.actual.type == "LBRACE":
            tokens.selectNext()
            while tokens.actual.type != "RBRACE":
                result.append(Parser.parseCommand())
        else:
            raise Exception("[-] unexpected token.")

        tokens.selectNext()
        return Commands(None, result)

    @staticmethod
    def parseCommand():
        tokens = Parser.tokens

        if tokens.actual.type == "IDENTIFIER":
            result = Assignment(tokens.actual.value)
            tokens.selectNext()
            if tokens.actual.type != "EQUAL":
                raise Exception("[-] unexpected token.")
            tokens.selectNext()
            result.children = [Parser.parseExpression()]

        elif tokens.actual.type == "COMMAND":
            value = tokens.actual.value
            tokens.selectNext()
            result = Echo(value, [Parser.parseExpression()])

        elif tokens.actual.type == "SEMI":
            tokens.selectNext()
            return NoOp(None)
        else:
            return Parser.parseBlock()

        if tokens.actual.type != "SEMI":
            raise Exception("[-] unexpected token.")
        tokens.selectNext()
        return result

    @staticmethod
    def parseFactor():
        tokens = Parser.tokens
        result = None
        if tokens.actual.type == "INT":
            result = IntVal(int(tokens.actual.value))
            tokens.selectNext()
        elif tokens.actual.type == "OPEN":
            tokens.selectNext()
            result = Parser.parseExpression()
            if(tokens.actual.type != "CLOSE"):
                raise Exception("[-] unexpected token.")
            tokens.selectNext()
        elif tokens.actual.type == "PLUS":
            tokens.selectNext()
            result = UnOp("PLUS", [Parser.parseFactor()])
        elif tokens.actual.type == "MINUS":
            tokens.selectNext()
            result = UnOp("MINUS", [Parser.parseFactor()])
        elif tokens.actual.type == "IDENTIFIER":
            result = Identifier(tokens.actual.value)
            tokens.selectNext()
        else:
            raise Exception("[-] unexpected token.")

        return result

    @staticmethod
    def parseTerm():
        tokens = Parser.tokens
        result = Parser.parseFactor()

        while tokens.actual.type in ["DIVIDE", "MULTIPLY"]:
            if tokens.actual.type == "MULTIPLY":
                tokens.selectNext()
                result = BinOp("MULTIPLY", [result, Parser.parseFactor()])
            elif tokens.actual.type == "DIVIDE":
                tokens.selectNext()
                result = BinOp("DIVIDE", [result, Parser.parseFactor()])
        return result

    @staticmethod
    def parseExpression():
        tokens = Parser.tokens
        result = Parser.parseTerm()
        while tokens.actual.type in ["PLUS", "MINUS"]:
            if tokens.actual.type == "PLUS":
                tokens.selectNext()
                result = BinOp("PLUS", [result, Parser.parseTerm()])
            elif tokens.actual.type == "MINUS":
                tokens.selectNext()
                result = BinOp("MINUS", [result, Parser.parseTerm()])
        return result

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        parsed = Parser.parseBlock()
        if Parser.tokens.actual.type != "EOF":
            raise Exception("[-] unexpected token")
        return parsed
