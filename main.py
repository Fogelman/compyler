import sys
from parser import Parser
from preprocessor import Preprocessor

code = sys.argv[1]
preprocessed = Preprocessor.run(code)
parsed = Parser.run(preprocessed)
print(parsed.Evaluate())
