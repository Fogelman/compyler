# https://joshsharp.com.au/blog/rpython-rply-interpreter-1.html
from compyler import _run
code = """ABACATE = 11-12
if(True){
    print(ABACATE)
}else{
    print(5*(1*2*4+2))
}

a = 5
while (a!=2){
    a = a-1
    print(a)
}
"""
result = _run(code)
