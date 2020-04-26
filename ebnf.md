```
input: (NEWLINE | stmt)*
funcdef: 'def' NAME arglist suite

exprlist: expr (',' expr)* [',']
testlist: test (',' test)* [',']
arglist: '(' argument (',' argument)* ')'
argument: NAME

suite: '{' stmt+ '}'
stmt: simple_stmt | compound_stmt
simple_stmt: (small_stmt NEWLINE)+
small_stmt: (expr_stmt | return_stmt )
expr_stmt: testlist_expr [('=' (testlist_expr))+]
return_stmt: 'return' [testlist_expr]

compound_stmt: if_stmt | while_stmt | funcdef | print_stmt
if_stmt: 'if' test suite ('elif' test suite)* ['else' suite]
while_stmt: 'while' test suite ['else' suite]
print_stmt: 'print' '(' (test|expr) ')'
testlist_expr: (test|expr) (',' (test|expr))* [',']


test: and_test ('or' and_test)*
and_test: not_test ('and' not_test)*
not_test: 'not' not_test | comparison
comparison: bitwise (('<'|'>'|'=='|'>='|'<='|'!=') bitwise)*
bitwise: arith | (arith ('|', '^', '&') bitwise)
arith: term | (term ('+'|'-') arith)
term: factor | (factor ('*'|'/'|'%'|'//') term)
factor: ('+'|'-'|'~') factor | atom
atom: '(' test ')' | NAME | NUMBER | 'None' | 'True' | 'False'
```
