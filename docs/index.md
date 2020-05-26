# Getting started

A language for those who think python could be made a little bit more difficult. If you're new here check the example below.


## Example

!!! warning 
    Follow first the [requirements](src/requirements/#requirements) to set up the enviroment.

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



Copy the block above and save in `program.x`. Save in the same directory of main.py.


### Compile

Execute the following command to compile the `program.x` file to `output.o`

    python main.py program.x output.o

### Create executable

We can use gcc to transform the `output.o` file to an executable using:

    gcc output.o -o output

### Running

If everything runs smoothly you should have an executable by now. Just run:

    ./output