from tokenizer import Tokenizer


class Parser:
    tokens = None

    @staticmethod
    def parseFactor():
        tokens = Parser.tokens
        tokens.selectNext()
        if tokens.actual.type == "INT":
            result = int(tokens.actual.value)
            tokens.selectNext()
            return result
        elif(tokens.actual.type == "OPEN"):
            result = Parser.parseExpression()
            if(tokens.actual.type != "CLOSE"):
                raise Exception("[-] unexpected token.")
            tokens.selectNext()
            return result
        elif(tokens.actual.type == "PLUS"):
            return Parser.parseFactor()
        elif(tokens.actual.type == "MINUS"):
            return -Parser.parseFactor()
        else:
            raise Exception("[-] unexpected token.")

    @staticmethod
    def parseTerm():
        tokens = Parser.tokens
        result = Parser.parseFactor()

        while tokens.actual.type in ["DIVIDE", "MULTIPLY"]:
            if tokens.actual.type == "MULTIPLY":
                result *= Parser.parseFactor()
            elif tokens.actual.type == "DIVIDE":
                result /= Parser.parseFactor()
        return result

    @staticmethod
    def parseExpression():
        tokens = Parser.tokens
        result = Parser.parseTerm()

        while tokens.actual.type in ["PLUS", "MINUS"]:
            if tokens.actual.type == "PLUS":
                result += Parser.parseTerm()
            elif tokens.actual.type == "MINUS":
                result -= Parser.parseTerm()
        return result

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        parsed = Parser.parseExpression()
        if Parser.tokens.actual.type != "EOF":
            raise Exception("[-] unexpected token")
        return parsed
