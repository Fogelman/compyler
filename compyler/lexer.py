from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add(self):
        self.lexer.add('INTEGER', r'\d+')
        self.lexer.add('BOOLEAN', r'True(?!\w)|False(?!\w)')
        self.lexer.add('NONE', r'None(?!\w)')
        self.lexer.add('IF', r'isit(?!\w)')
        self.lexer.add('ELSE', r'other(?!\w)')
        self.lexer.add('WHILE', r'during(?!\w)')
        self.lexer.add('DEF', r'hmmm(?!\w)')
        self.lexer.add('AND', r'and(?!\w)')
        self.lexer.add('OR', r'or(?!\w)')
        self.lexer.add('NOT', r'not(?!\w)')
        self.lexer.add('RETURN', r'return(?!\w)')
        self.lexer.add('PRINT', r'print(?!\w)')
        self.lexer.add('=', r'fifty\-fifty(?!\w)')
        self.lexer.add('//', r'\/\/')
        self.lexer.add('==', r'\=\=')
        self.lexer.add('!=', r'\!\=')
        self.lexer.add('>=', r'\>\=')
        self.lexer.add('<=', r'\<\=')
        self.lexer.add('<', r'\<')
        self.lexer.add('~', r'\~')
        self.lexer.add('>', r'\>')
        self.lexer.add('{', r'\{')
        self.lexer.add('}', r'\}')
        self.lexer.add('|', r'\|')
        self.lexer.add('&', r'\&')
        self.lexer.add('^', r'\^')
        self.lexer.add('COMMA', r'\,')
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('MINUS', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')
        self.lexer.add('MOD', r'\%')
        self.lexer.add('OPEN', r'\(')
        self.lexer.add('CLOSE', r'\)')
        self.lexer.add('NEWLINE', '\n')
        self.lexer.add('IDENTIFIER', r"[a-zA-Z_][a-zA-Z0-9_]*")

        # ignore whitespaces (excluding \n)
        self.lexer.ignore(r'[ \t\r\f\v]+')

    def get(self):
        self._add()
        return self.lexer.build()
