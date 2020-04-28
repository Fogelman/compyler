# https://joshsharp.com.au/blog/rpython-rply-interpreter-1.html
from compyler import _run
code = """
def abc(test , askjdkas){\nprint(1)\nif(test ==2){\n    print(123123)\n}}\nabc(2,2)
"""
result = _run(code)
