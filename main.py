import sys
import os
from compyler.parser import Parser
from compyler.preprocessor import Preprocessor

path = sys.argv[1]

with open(os.path.abspath(path), "r") as file:
    code = file.read()

preprocessed = Preprocessor.run(code)
parsed = Parser.run(preprocessed)
evaluated = parsed.Evaluate()
print(evaluated)
