
__author__ = "David Fogelman"
__license__ = "MIT"
__version__ = "2.0.3"
__maintainer__ = "David Fogelman"
__status__ = "Production"

__all__ = ['node',
           'parser',
           'preprocessor',
           'token',
           'tokenizer']

from compyler.parser import Parser
from compyler.preprocessor import Preprocessor


def _run(code):
    preprocessed = Preprocessor.run(code)
    parsed = Parser.run(preprocessed)
    evaluated = parsed.Evaluate()
    return evaluated
