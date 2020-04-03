import pytest
from compyler import _run

tests = [
    ("""
{
$x = 2;
$z = $x + 3;
$z = $z - 3;
echo ($z+1)*2;
}
    """, "6"),
    ("""
{
$x = 2;
echo $x;
}
    """, "2"),
    ("""
{
$x = 2;
ECHO $x;
}
    """, "2"),
    ("""
{
$x = -(2  +  3)/5;
$y = $x + 5;
echo $x*$y+3- -2/4;
}
    """, "0"),
    ("""
{
$x = -(2  +  3)/5;
$y = $x + 5;
ECHO $x*$y+3- -2/4;
}
    """, "0"),
    ("""
{
$x = 1
}
    """, None),

    ("""
{
$x = 1;
}
    """, "")
]


@pytest.mark.parametrize("input,output", tests)
def test_result(input, output, capsys):
    if output is None:
        with pytest.raises(Exception):
            _run(input)
    else:
        _run(input)
        captured = capsys.readouterr()
        assert captured.out == output
