from tokenizer import Tokenizer


class Parser:
    tokens = None

    @staticmethod
    def parseExpression():
        Parser.tokens.selectNext()
        # while Parser.tokens.actual.type != "EOF":
        #     print(Parser.tokens.actual.value)
        #     Parser.tokens.selectNext()

        currentToken = Parser.tokens.actual
        result = 0
        if(currentToken.type == "INT"):
            pass
        else:
            raise Exception(
                "[-] ERROR Could not decode input. Check semantics.")

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.parseExpression()
