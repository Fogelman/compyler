# https://joshsharp.com.au/blog/rpython-rply-interpreter-1.html
from compyler import _run
code = """print(1-1)
"""
result = _run(code)
