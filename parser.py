from tokenizer import Tokenizer


class Parser:
    tokens = None

    @staticmethod
    def parseExpression():
        tokens = Parser.tokens
        tokens.selectNext()
        result = 0

        if(tokens.actual.type == "INT"):
            result = int(tokens.actual.value)
            tokens.selectNext()

            while not tokens.actual.type == "EOF":
                if tokens.actual.type == "PLUS":
                    tokens.selectNext()
                    if tokens.actual.type == "INT":
                        result += int(tokens.actual.value)
                    else:
                        raise Exception("[-] Could not decode input.")
                elif tokens.actual.type == "MINUS":
                    tokens.selectNext()
                    if tokens.actual.type == "INT":
                        result -= int(tokens.actual.value)
                    else:
                        raise Exception("[-] Could not decode input.")
                else:
                    raise Exception("[-] Could not decode input.")
                tokens.selectNext()

            return result
        else:
            raise Exception(
                "[-] ERROR Could not decode input.")

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        parsed = Parser.parseExpression()
        return parsed
