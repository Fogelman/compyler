import sys
from parser import Parser

code = sys.argv[1]
parsed = Parser.run(code)
print(parsed)
