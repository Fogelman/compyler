# https://joshsharp.com.au/blog/rpython-rply-interpreter-1.html
import sys
from compyler import _run

with open(sys.argv[1], "r") as file:
    code = file.read()

result = _run(code, sys.argv[2])
