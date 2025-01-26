from termcolor import colored

from hell import T as T_orig
from tests.capture_out import capture_out


T = capture_out(T_orig)


def test_arg():
    assert T('') == colored("<class 'str'>\n")
    assert T(1) == colored("<class 'int'>\n")


def test_c():
    assert T(object, c='green') == colored("<class 'type'>\n", 'green')
    assert T(type, c='b') == colored("<class 'type'>\n", 'blue')


def test_b():
    assert T({}, b='green') == colored("<class 'dict'>\n", on_color='on_green')


def test_a_str():
    assert T(0.0, a='underline') == colored("<class 'float'>\n", attrs=['underline'])


def test_a_short_list():
    assert T(None, a=['u']) == colored("<class 'NoneType'>\n", attrs=['underline'])


def test_pipe():
    assert 123 | T_orig is int


def test_all():
    attrs = ['bold', 'underline']
    assert T(9, c='red', b='blue', a=attrs) == colored("<class 'int'>\n", 'red', 'on_blue',
                                                       attrs=attrs)
