from tokenizer import Tokenizer


class Parser:
    tokens = None

    @staticmethod
    def parseTerm():
        tokens = Parser.tokens
        tokens.selectNext()
        result = 0

        if(tokens.actual.type == "INT"):
            result = int(tokens.actual.value)
            tokens.selectNext()

            while tokens.actual.type in ["DIVIDE", "MULTIPLY"]:
                if tokens.actual.type == "MULTIPLY":
                    tokens.selectNext()
                    if tokens.actual.type == "INT":
                        result *= int(tokens.actual.value)
                    else:
                        raise Exception("[-] unexpected token.")
                elif tokens.actual.type == "DIVIDE":
                    tokens.selectNext()
                    if tokens.actual.type == "INT":
                        result /= int(tokens.actual.value)
                    else:
                        raise Exception("[-] unexpected token.")
                tokens.selectNext()
            return result
        else:
            raise Exception(
                "[-] unexpected token.")

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
