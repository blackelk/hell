from termcolor import colored

from hell import M
from conftest import capture_out


m = capture_out(M)


def test_arg_zero():
    assert m(0) == colored('int | object\n')


def test_arg_int():
    assert m(int) == colored('int | object\n')


def test_arg_bool():
    assert m(bool) == colored('bool | int | object\n')


def test_arg_type():
    assert m(type) == colored('type | object\n')


def test_sep():
    assert m(0, sep=', ') == colored('int, object\n')


def test_c():
    assert m(1, c='green') == colored('int | object\n', 'green')


def test_b():
    assert m(None, b='green') == colored('NoneType | object\n', on_color='on_green')


def test_a():
    assert m({}, a=['underline']) == colored('dict | object\n', attrs=['underline'])


def test_all():
    attrs = ['bold', 'underline']
    expected = colored('list, object\n', 'red', 'on_blue', attrs=attrs)
    result = m([], sep=', ', c='red', b='blue', a=attrs)

    assert expected == result
