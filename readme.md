# compyler

[![Build Status](https://travis-ci.com/Fogelman/compyler.svg?token=m4KMpTsinBJNfZSW8czm&branch=master)](https://travis-ci.com/Fogelman/compyler)

```
EBNF

BLOCK = "{", { COMMAND }, "}" ;
COMMAND = ( λ | ASSIGNMENT | PRINT), ";" | BLOCK ;
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;
PRINT = "echo", EXPRESSION ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;
IDENTIFIER = "$", LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```
