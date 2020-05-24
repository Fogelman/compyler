# compyler

[![Build Status](https://travis-ci.com/Fogelman/compyler.svg?token=m4KMpTsinBJNfZSW8czm&branch=master)](https://travis-ci.com/Fogelman/compyler)

```
EBNF

BLOCK = "{", { COMMAND }, "}" ;
COMMAND = ( λ | ASSIGNMENT | ECHO), ";" | BLOCK | WHILE | IF | FUNCALL;
FUNCALL = NAME "(", [RELEXPR | RELEXPR , {"," , RELEXPR}] ")";
FUNDEF = "function" NAME "(", [IDENTIFIER | IDENTIFIER , {"," , IDENTIFIER}] ")" , COMMAND ;
ASSIGNMENT = IDENTIFIER, "=", RELEXPR ;
ECHO = "ECHO", RELEXPR ;
IF = "IF", "(", RELEXPR, ")", COMMAND ["ELSE", COMMAND];
WHILE = "WHILE", "(", RELEXPR, ")", COMMAND;
RELEXPR = EXPRESSION, {("==" | ">" | "<" | ">=" | "<="), EXPRESSION} ;
EXPRESSION = TERM, {("+" | "-" | "OR" | "."), TERM } ;
TERM = FACTOR, {("*" | "/" | "AND"), FACTOR } ;
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | "(", RELEXPR, ")" | IDENTIFIER | "READLINE", "(", ")" | "True" | "False" | STRING | FUNCALL" ;
IDENTIFIER = "$", LETTER, { LETTER | DIGIT | "_" } ;
NAME = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
STRING = """ {.*?} """;
```
