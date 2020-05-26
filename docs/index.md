# Getting started

A language for those who think python could be made a little bit more difficult. If you're new here check the example below.

## Example

Lets write some code to calculate Fibonacci sequence.

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



!!! important

    Copy the block above and save in `program.x`. Save in the same directory of main.py.


### Compile

Execute the following command to compile the `program.x` file to `output.o`

    python main.py program.x output.o