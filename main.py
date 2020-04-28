# https://joshsharp.com.au/blog/rpython-rply-interpreter-1.html
from compyler import _run
code = """

def abc(test , askjdkas){
    print(1)

    if(test ==2){
        print(123123)
    }

    return 1
}

c  = abc(2,2)
print(c)
"""
result = _run(code)
