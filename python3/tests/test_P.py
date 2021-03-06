from hell import P
from conftest import capture_out


p = capture_out(P)


def test_args():

    assert p() == '\n'
    assert p('') == '\n'
    assert p('A') == 'A\n'
    assert p(1) == '1\n'
    assert p('A', 1) == 'A 1\n'
    assert p([0, 1, 'A']) == "[0, 1, 'A']\n"


def test_kwargs():

    assert p('', end= '.') == '.'
    assert p('A', sep= '|') == 'A\n'
    assert p('A', 1, sep= '|') == 'A|1\n'
    assert p('A', 1, end='.', sep='|') == 'A|1.'

