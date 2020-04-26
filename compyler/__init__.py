
__author__ = "David Fogelman"
__license__ = "MIT"
__version__ = "2.2.1"
__maintainer__ = "David Fogelman"
__status__ = "Production"

__all__ = [
    'parser',
    'lexer', ]


def _run(code):
    from compyler.lexer import Lexer
    from compyler.parser import Parser
    from compyler.symboltable import SymbolTable

    lexer = Lexer().get()
    tokens = lexer.lex(code)
    st = SymbolTable()
    parser = Parser().build()

    parser.parse(tokens).Evaluate(st)
