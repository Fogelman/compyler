from compyler.tokenizer import Tokenizer
from compyler.node import BinOp, UnOp, IntVal, NoOp


class Parser:
    tokens = None

    @staticmethod
    def parseFactor():
        tokens = Parser.tokens
        tokens.selectNext()
        result = None
        if tokens.actual.type == "INT":
            result = IntVal(int(tokens.actual.value))
            tokens.selectNext()
        elif(tokens.actual.type == "OPEN"):
            result = Parser.parseExpression()
            if(tokens.actual.type != "CLOSE"):
                raise Exception("[-] unexpected token.")
            tokens.selectNext()
        elif(tokens.actual.type == "PLUS"):
            result = UnOp("PLUS", [Parser.parseFactor()])
        elif(tokens.actual.type == "MINUS"):
            result = UnOp("MINUS", [Parser.parseFactor()])

        else:
            raise Exception("[-] unexpected token.")

        return result

    @staticmethod
    def parseTerm():
        tokens = Parser.tokens
        result = Parser.parseFactor()

        while tokens.actual.type in ["DIVIDE", "MULTIPLY"]:
            if tokens.actual.type == "MULTIPLY":
                result = BinOp("MULTIPLY", [result, Parser.parseFactor()])
            elif tokens.actual.type == "DIVIDE":
                result = BinOp("DIVIDE", [result, Parser.parseFactor()])
        return result

    @staticmethod
    def parseExpression():
        tokens = Parser.tokens
        result = Parser.parseTerm()
        while tokens.actual.type in ["PLUS", "MINUS"]:
            if tokens.actual.type == "PLUS":
                result = BinOp("PLUS", [result, Parser.parseTerm()])
            elif tokens.actual.type == "MINUS":
                result = BinOp("MINUS", [result, Parser.parseTerm()])
        return result

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        parsed = Parser.parseExpression()
        if Parser.tokens.actual.type != "EOF":
            raise Exception("[-] unexpected token")

        return parsed
