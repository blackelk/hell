from pytest import raises
from termcolor import colored

from hell import L
from conftest import capture_out


l = capture_out(L)


def test_arg():
    assert l('') == colored('0\n')
    assert l([1]) == colored('1\n')


def test_c():
    assert l('A', c='green') == colored('1\n', 'green')
    assert l('A', c='b') == colored('1\n', 'blue')


def test_b():
    assert l({}, b='green') == colored('0\n', on_color='on_green')


def test_a_str():
    assert l({1, 2}, a='underline') == colored('2\n', attrs=['underline'])


def test_all():
    attrs = ['bold', 'underline']
    assert l([0], c='red', b='blue', a=attrs) == colored('1\n', 'red', 'on_blue', attrs=attrs)


def test_raises():
    with raises(TypeError):
        L(0)

