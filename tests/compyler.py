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
    """, "6")
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
