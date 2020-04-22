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
    """, "6\n"),
    ("""
{
$x = 2;
echo $x;
}
    """, "2\n"),
    ("""
{
$x = 2;
ECHO $x;
}
    """, "2\n"),
    ("""
{
$x = -(2  +  3)/5;
$y = $x + 5;
echo $x*$y+3- -2/4;
}
    """, "0\n"),
    ("""
{
$x = -(2  +  3)/5;
$y = $x + 5;
ECHO $x*$y+3- -2/4;
}
    """, "0\n"),
    ("""
{
$x = 1
}
    """, None),

    ("""
{
$x = 1;
}
    """, ""),

    ("""{
    {   
    $a = 8;
	echo $a;
	$b = 2 + $a;
	echo $b;
	$a = $b;
	echo $a;
    }
}""", "8\n10\n10\n"),

    ("""
{
    ;
}""", ""),
    ("""
{
    {;}
}""", ""),
    ("""

/*

Hello World!

*/

{
    {;}
}""", ""),
    ("""

/*

Hello World!

*/

{
    $a = 123;
    if(1==1){echo $a;}
}""", "123\n"),
    ("""

/*

Hello World!

*/

{
    if(1==1){echo 123;}
}""", "123\n"),
    ("""

/*

Hello World!

*/

{
    if(1==2){echo 123;}
}""", ""),
    ("""
    {
    $a = 3;
    while($a>0){
        echo 123;
        $a = $a - 1;
    }
    }
""", "123\n123\n123\n")
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
