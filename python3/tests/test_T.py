from termcolor import colored

from hell import T
from conftest import capture_out


t = capture_out(T)


def test_arg():
    assert t('') == colored("<class 'str'>\n")
    assert t(1) == colored("<class 'int'>\n")


def test_c():
    assert t(object, c='green') == colored("<class 'type'>\n", 'green')
    assert t(type, c='b') == colored("<class 'type'>\n", 'blue')


def test_b():
    assert t({}, b='green') == colored("<class 'dict'>\n", on_color='on_green')


def test_a_str():
    assert t(0.0, a='underline') == colored("<class 'float'>\n", attrs=['underline'])


def test_a_short_list():
    assert t(None, a=['u']) == colored("<class 'NoneType'>\n", attrs=['underline'])


def test_all():
    attrs = ['bold', 'underline']
    assert t(9, c='red', b='blue', a=attrs) == colored("<class 'int'>\n", 'red', 'on_blue',
                                                       attrs=attrs)

