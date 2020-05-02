from compyler.tokenizer import Tokenizer
from compyler.node import BinOp, UnOp, IntVal, BoolVal, NoOp, Identifier, Assignment, Commands, Echo, NoOp, If, While, ReadLine, StringVal


class Parser:
    tokens = None

    @staticmethod
    def parseProgram():
        tokens = Parser.tokens
        result = []
        if tokens.actual.value == "<?PHP":
            tokens.selectNext()
            while tokens.actual.value != "?>":
                result.append(Parser.parseCommand())
        else:
            raise Exception("[-] unexpected token.")

        tokens.selectNext()
        return Commands(None, result)

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
            result.children = [Parser.parseRelationalExpression()]

        elif tokens.actual.value == "ECHO":
            value = tokens.actual.value
            tokens.selectNext()
            result = Echo(value, [Parser.parseRelationalExpression()])

        elif tokens.actual.value == "IF":
            tokens.selectNext()
            if tokens.actual.type == "OPEN":
                tokens.selectNext()
                relexpr = Parser.parseRelationalExpression()

                if(tokens.actual.type != "CLOSE"):
                    raise Exception("[-] unexpected token.")
                tokens.selectNext()
                command = Parser.parseCommand()

                if tokens.actual.value == "ELSE":
                    tokens.selectNext()
                    return If(
                        None, [relexpr, command, Parser.parseCommand()])

                return If(None, [relexpr, command])
            else:
                raise Exception("[-] unexpected token.")

        elif tokens.actual.value == "WHILE":
            tokens.selectNext()
            if tokens.actual.type == "OPEN":
                tokens.selectNext()
                relexpr = Parser.parseRelationalExpression()
                if(tokens.actual.type != "CLOSE"):
                    raise Exception("[-] unexpected token.")
                tokens.selectNext()
                command = Parser.parseCommand()
                return While(None, [relexpr, command])
            else:
                raise Exception("[-] unexpected token.")
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
        elif tokens.actual.type == "BOOLEAN":
            result = BoolVal(tokens.actual.value == "TRUE")
            tokens.selectNext()
        elif tokens.actual.type == "OPEN":
            tokens.selectNext()
            result = Parser.parseRelationalExpression()
            if(tokens.actual.type != "CLOSE"):
                raise Exception("[-] unexpected token.")
            tokens.selectNext()
        elif tokens.actual.type == "PLUS":
            tokens.selectNext()
            result = UnOp("+", [Parser.parseFactor()])
        elif tokens.actual.type == "MINUS":
            tokens.selectNext()
            result = UnOp("-", [Parser.parseFactor()])
        elif tokens.actual.type == "NOT":
            tokens.selectNext()
            result = UnOp("NOT", [Parser.parseFactor()])
        elif tokens.actual.value == "READLINE":
            tokens.selectNext()
            result = ReadLine(None, [])
            if(tokens.actual.type != "OPEN"):
                raise Exception("[-] unexpected token.")
            tokens.selectNext()
            if(tokens.actual.type != "CLOSE"):
                raise Exception("[-] unexpected token.")
            tokens.selectNext()
        elif tokens.actual.type == "IDENTIFIER":
            result = Identifier(tokens.actual.value)
            tokens.selectNext()
        elif tokens.actual.type == "STRING":
            result = StringVal(tokens.actual.value)
            tokens.selectNext()
        else:
            raise Exception("[-] unexpected token.")

        return result

    @staticmethod
    def parseTerm():
        tokens = Parser.tokens
        result = Parser.parseFactor()

        while tokens.actual.value in ["/", "*", "AND"]:

            value = tokens.actual.value
            tokens.selectNext()
            result = BinOp(value, [result, Parser.parseFactor()])
        return result

    @staticmethod
    def parseExpression():
        tokens = Parser.tokens
        result = Parser.parseTerm()
        while tokens.actual.value in ["+", "-", "OR", "."]:

            value = tokens.actual.value
            tokens.selectNext()
            result = BinOp(value, [result, Parser.parseTerm()])
        return result

    @staticmethod
    def parseRelationalExpression():
        tokens = Parser.tokens
        result = Parser.parseExpression()
        while tokens.actual.value in ["==", ">", "<", ">=", "<="]:
            value = tokens.actual.value
            tokens.selectNext()
            result = BinOp(value, [result, Parser.parseExpression()])
        return result

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        parsed = Parser.parseProgram()
        if Parser.tokens.actual.type != "EOF":
            raise Exception("[-] unexpected token")
        return parsed
