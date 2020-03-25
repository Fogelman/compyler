import pytest
from compyler.parser import Parser
from compyler.preprocessor import Preprocessor

tests = [
    ("(1+/*A */1)*10", "20"),
    ("(((1+1)))", "2"),
    ("21+21", "42"),
    ("100 + 100 -  100+1", "101"),
    ("--2", "2"),
    ("8  * 9 / 2", "36"),
    ("1*1", "1"),
    ("40+++++++++2", "42"),
    ("/* A */ 1 /* A */", "1"),
    ("50-150", "-100"),
    ("44---2", "42"),
    ("(1+1)*3", "6"),
    ("100 + 100", "200"),
    ("1 1", None),
    (",", None),
    ("1+(1", None),
    ("(10*(9*9))", "810"),
    ("- -2", "2"),
    ("2+5*4", "22"),
    ("32*985", "31520"),
    ("1 + /* A */ */", None),
    ("1/2", "0"),
    ("1/1", "1"),
    ("1-1", "0"),
    ("1 + /* 2 */ 3", "4"),
    ("0/1", "0"),
    ("(1+1)*(2+2)", "8"),
    ("4//2", None),
    ("/* A 1", None),
    ("(1+(1)", None),
    ("1+1", "2"),
    ("1+", None),
    ("(1-(1)", None),
    ("/* A /* 1 */ 2", "2"),
    ("1+1)", None),
    ("40+-+-2", "42"),
    ("100 + 100 -  100+1                                               -101                  - 900", "-900"),
    ("8//4**2", None),
    ("3**3", None),
    ("1 /* A", None),
    ("3168/99", "32"),
    ("-1", "-1"),
    ("40--2", "42"),
    ("2*4/2", "4"),
    ("--2+40", "42"),
    ("""1+1
(3 + 2)/  5
+--++3
-  - 5
3-  -2/4
(2*2)
(2*2
2*2)""", None)
]


def run(code):
    preprocessed = Preprocessor.run(code)
    parsed = Parser.run(preprocessed)
    evaluated = parsed.Evaluate()
    return evaluated


@pytest.mark.parametrize("input,output", tests)
def test_result(input, output):
    if output is None:
        with pytest.raises(Exception):
            run(input)
    else:
        assert str(run(input)) == output
