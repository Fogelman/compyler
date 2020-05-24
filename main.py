# https://joshsharp.com.au/blog/rpython-rply-interpreter-1.html
from compyler import _run
code = r"""
a fifty-fifty 6
a fifty-fifty a + 2
print(a)

hmmm abc(test , askjdkas){
    test fifty-fifty test +5
isit(test ==2){
    askjdkas fifty-fifty askjdkas*2
}
return 0
}

"""
result = _run(code)


with open("output.o", "wb") as file:
    file.write(result)

# def fibbonacci(n):
#     if(n == 0):
#         return 0
#     else:
#         if(n == 1):
#             return 1
#         else:
#             return (fibbonacci(n-1) + fibbonacci(n-2))


# print(fibbonacci(10))
