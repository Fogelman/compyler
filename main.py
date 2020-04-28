# https://joshsharp.com.au/blog/rpython-rply-interpreter-1.html
from compyler import _run
code = """


def fibbonacci(n) {
   if(n == 0){
      return 0
   } else{
        if(n == 1) {
            return 1
        } else {
            return (fibbonacci(n-1) + fibbonacci(n-2))
        }
   }
}

c  = fibbonacci(10)
print(c)
"""
result = _run(code)


def fibbonacci(n):
    if(n == 0):
        return 0
    else:
        if(n == 1):
            return 1
        else:
            return (fibbonacci(n-1) + fibbonacci(n-2))


print(fibbonacci(10))
