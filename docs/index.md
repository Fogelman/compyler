# Getting started

A language for those who think python could be made a little bit more difficult. If you're new here check the [example](./src/examples/#examples) section.

##  Context

This language started due to a subject at <a href="https://www.insper.edu.br/en/" target="_blank">insper</a>. As the day of creation of this language, there aren't many examples or guides on how to use <a href="https://llvmlite.readthedocs.io/en/latest/" target="_blank">llvmlite</a>, a python implementation of the original <a href="https://llvm.org/" target="_blank">llvm</a>. I've tried to make this project organized and with tests to make sure that others interessed can have an easier path in.

## Motivation

<div style="text-align: justify"> But why build a new language? Let me answer that with: why not? Thats the aproach of the language, throwing some sarcasm around. With so many languages been born and more heated discussions about which is the most efficient and easier to write, I've created a baseline on what is inefficient and hard to write, so everything above should be "OK" to use. </div>


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