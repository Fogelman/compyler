import os
import builtins
import json
import pytest
from compyler import _run


cwd = os.getcwd()
with open(os.path.join(cwd, "tests", "tests.json"), "r") as file:
    raw = json.load(file)

"""
Convert the list of dictionaries into tuple. There is no garanty of order. Only if it's an OrderDict
"""
tests = [[values for values in test.values()]
         for test in raw]


def finput(inputs):
    """
    Receive list of inputs and return on each call
    """
    for i in inputs:
        yield i


@pytest.mark.parametrize("code, expect, inputs", tests)
def test_result(code, expect, inputs, capsys, monkeypatch):
    generator = finput(inputs)
    def mock(text=None): return next(generator)
    with monkeypatch.context() as m:
        m.setattr(builtins, 'input', mock)
        if expect is None:
            with pytest.raises(Exception):
                _run(code)
        else:
            _run(code)
            captured = capsys.readouterr()
            assert captured.out == expect
