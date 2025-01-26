from hell import P as P_orig
from tests.capture_out import capture_out


P = capture_out(P_orig)


def test_args():
    assert P() == '\n'
    assert P('') == '\n'
    assert P('A') == 'A\n'
    assert P(1) == '1\n'
    assert P('A', 1) == 'A 1\n'
    assert P([0, 1, 'A']) == "[0, 1, 'A']\n"


def test_kwargs():
    assert P('', end= '.') == '.'
    assert P('A', sep= '|') == 'A\n'
    assert P('A', 1, sep= '|') == 'A|1\n'
    assert P('A', 1, end='.', sep='|') == 'A|1.'
