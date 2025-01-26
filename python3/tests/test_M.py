from termcolor import colored

from hell import M as M_orig
from tests.capture_out import capture_out


M = capture_out(M_orig)


def test_arg_zero():
    assert M(0) == colored('int | object\n')


def test_arg_int():
    assert M(int) == colored('int | object\n')


def test_arg_bool():
    assert M(bool) == colored('bool | int | object\n')


def test_arg_type():
    assert M(type) == colored('type | object\n')


def test_sep():
    assert M(0, sep=', ') == colored('int, object\n')


def test_c():
    assert M(1, c='green') == colored('int | object\n', 'green')


def test_b():
    expected = colored('NoneType | object\n', on_color='on_green')
    assert M(None, b='green') == expected


def test_a():
    expected = colored('dict | object\n', attrs=['underline'])
    assert M({}, a=['underline']) == expected


def test_all():
    attrs = ['bold', 'underline']
    expected = colored('list, object\n', 'red', 'on_blue', attrs=attrs)
    result = M([], sep=', ', c='red', b='blue', a=attrs)

    assert expected == result
