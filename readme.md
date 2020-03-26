# compyler

[![Build Status](https://travis-ci.com/Fogelman/compyler.svg?token=m4KMpTsinBJNfZSW8czm&branch=master)](https://travis-ci.com/Fogelman/compyler)

```
EBNF

digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
number = digit, {digit};
exp = term, { [ "-" | "+" ], term};
term = factor, {["/" | "*"], number};
factor = number | "(", exp, ")" | ["+"|"-"], factor;
```
