# compyler

```
EBNF

digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
number = {digit}
exp = term, { [ "-" | "+" ], term}
term = number, {["/" | "*"], number}
```