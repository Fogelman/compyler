# https://joshsharp.com.au/blog/rpython-rply-interpreter-1.html
import sys
from compyler import _run
code = r"""
hmmm fibbonacci(n) {
    isit(n == 0){
       return 0
} other{
         isit(n == 1) {
             return 1
} other {
             return (fibbonacci(n-1) + fibbonacci(n-2))
     }}
return 0
}
 c  fifty-fifty fibbonacci(35) 
 print(c)

"""
result = _run(code)

sys.stdout = open('file.txt', 'w')
with open("output.o", "wb") as file:
    file.write(result)
