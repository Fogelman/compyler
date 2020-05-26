# Getting started

A language for those who think python could be made a little bit more difficult. If you're new here check the [example](./src/examples/#examples) section.

##  Context

This language started due to a subject at <a href="https://www.insper.edu.br/en/" target="_blank">insper</a>.

## Motivation

But why build a new language? Let me answer that with: why not? Thats the aproach of the language, throwing some sarcasm around.


## Compile & Run

### Compile

Execute the following command to compile the `program.x` file to `output.o`
```
python main.py program.x output.o
```

### Create executable

We can use gcc to transform the `output.o` file to an executable using:
```
gcc output.o -o output
```

### Running

If everything runs smoothly you should have an executable by now. Just run:
```
./output
```