```
digit: "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
alfabet: "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z";
NEWLINE: "\n";
NUMBER: digit, {digit};
NAME: alfabet, {alfabet};
STRING: """, (alfabet|digit), {alfabet|digit};

input : stmt
if: "}", comparison, "fi", stmt, "}", ("}", comparison, "file",  stmt, "{")*,  ["}", "esle" stmt, "{"];
while: "}",comparison,"elihw", stmt, "{", ["}", "esle" stmt, "{"];
func:  "}",  args, NAME, "fed", stmt, [[NAME]], "nruter""{"

args: "(",test,")"
test: NAME (",",NAME)*

comp_op: '<'|'>'|'=='|'=<'|'=>'|'=!'
comparison: expr (comp_op expr)*
stmt: (inline-stmt, NEWLINE)* | if | while | funcdef

expr: {NUMBER, [ "-" | "+" | "*" | "/" | "**" | "\\"]}, factor, ;
factor: NUMBER | "(", expr, ")" |  factor, ["+"|"-"];

inline-stmt: assign | "(", NAME, ")tnirp" | call
assign: NAME, oassign, (NAME | NUMBER | STRING | expr | call)
call: "(", args, ")", NAME
oassign: '=' | '=+' | '=-' | '=*'

```
