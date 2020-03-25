import sys
from compyler.parser import Parser
from compyler.preprocessor import Preprocessor

code = sys.argv[1]
preprocessed = Preprocessor.run(code)
parsed = Parser.run(preprocessed)
print(parsed.Evaluate())
