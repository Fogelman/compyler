# compyler

A revolutionary language to make your life harder. Implemented with `rply` + `llvmlite`

[![Build Status](https://travis-ci.com/Fogelman/compyler.svg?token=m4KMpTsinBJNfZSW8czm&branch=APS)](https://travis-ci.com/Fogelman/compyler)

### Documentation

All documentation and examples can be found [here](https://fogelman.github.io/compyler)

### Requirements

```
python >= 3.x
make >= 4.x
pip
```

### Setup

```
pip install -r requirements.txt
```

### Test

All tests are listed in `./tests/tests.json`

```
make test
```

### Run

```
python main.py program.x output.o
gcc output.o -o output
./output
```

### EBNF

The EBNF can be found at `./ebnf.md`

### Project Structure

```
compyler/
├── __init__.py
├── assembler.py
├── lexer.py
├── node.py
├── parser.py
└── symboltable.py
```

### References

[Pykaleidoscope](https://github.com/eliben/pykaleidoscope)

[Printf implementation](https://gist.github.com/alendit/defe3d518cd8f3f3e28cb46708d4c9d6#file-call_printf-py-L35)

[Using RPython and RPly to build a language interpreter](https://joshsharp.com.au/blog/rpython-rply-interpreter-1.html)

[Writing your own programming language and compiler with Python](https://blog.usejournal.com/writing-your-own-programming-language-and-compiler-with-python-a468970ae6df)

[Python's full Grammar specification](https://docs.python.org/3/reference/grammar.html)

[joshsharp/python-braid lexer.py](https://github.com/joshsharp/python-braid/blob/master/lexer.py)

[radk0s/ply SymbolTable.py](https://github.com/radk0s/ply/blob/master/Symboltable.py)

[zjl233/moe parser.py](https://github.com/zjl233/moe/blob/master/src/parser.py)
