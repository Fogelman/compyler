# Examples

!!! warning 
    - Follow first the [requirements](src/requirements/#requirements) to set up the enviroment.
    - For this time, the language only supports `int32` type.

## Basic operations

Same as python, but with some restrictions. Check grammar(operations)

```
a = 1
b = a + b
```

## Print

This one is easy, same as python.
```
print(0)
```

## If

If can be implemented with or without else block. The condition is considered true if value is not equal to zero.

```
isit(b > 2){
    b = b*2
}
```
If & Else
```
isit(b > 2){
    b = b*2
}other{
    b = 0
}
```


## Function


Lets write some code to calculate Fibonacci sequence.

```
hmmm fibbonacci(n) {
    isit(n == 0){
    return 0
    } other{
        isit(n == 1) {
            return 1
    } other {
            return (fibbonacci(n-1) + fibbonacci(n-2))
    }}
}
c  fifty-fifty fibbonacci(35) 
print(c)
```



Copy the block above and save in `program.x`. Save in the same directory of main.py.

