from pytest import raises
from termcolor import colored

from hell import L as L_orig
from tests.capture_out import capture_out


L = capture_out(L_orig)


def test_arg():
    assert L('') == colored('0\n')
    assert L([1]) == colored('1\n')


def test_c():
    assert L('A', c='green') == colored('1\n', 'green')
    assert L('A', c='b') == colored('1\n', 'blue')


def test_b():
    assert L({}, b='green') == colored('0\n', on_color='on_green')


def test_a_str():
    assert L({1, 2}, a='underline') == colored('2\n', attrs=['underline'])


def test_all():
    attrs = ['bold', 'underline']
    expected = colored('1\n', 'red', 'on_blue', attrs=attrs)
    assert L([0], c='red', b='blue', a=attrs) == expected


def test_pipe():
    assert 'abc' | L_orig == 3


def test_raises():
    with raises(TypeError):
        L(0)
