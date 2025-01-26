from termcolor import colored

from hell import C as C_orig, Config
from tests.capture_out import capture_out


C = capture_out(C_orig)

default = Config.C_DEFAULT_COLOR


def test_args():
    assert C() == colored('\n', default)

    assert C('A') == colored('A\n', default)

    assert C(1) == colored('1\n', default)

    assert C(['a', 'b', 'c']) == colored("['a', 'b', 'c']\n", default)

    assert C(1, 2) == colored('1 2\n', default)


def test_sep_end():
    assert C(1, 2, sep='|') == colored('1|2\n', default)

    assert C(1, end='.') == colored('1.', default)

    assert C(1, sep='|', end='.') == colored('1.', default)


def test_c_none():
    assert C('A', c=None) == colored('A\n')


def test_c():
    assert C('A', c='white') == colored('A\n', 'white')


def test_b():
    assert C('A', c='yellow', b='green') == colored('A\n', 'yellow', 'on_green')


def test_on_b():
    assert C('A', c='magenta', b='on_green') == colored('A\n', 'magenta', 'on_green')


def test_a_str():
    assert C('A', c='grey', a='underline') == colored('A\n', 'grey', attrs=['underline'])


def test_a_list():
    assert C('A', c='cyan', a=['reverse']) == colored('A\n', 'cyan', attrs=['reverse'])

    assert C('A', c='red', a=['bold', 'dark']) == colored('A\n', 'red', attrs=['bold', 'dark'])


def test_shortcuts():
    assert C('A', c='b') == colored('A\n', 'blue')

    assert C('A', c='b', b='g') == colored('A\n', 'blue', 'on_green')

    assert C('A', c='b', a='b') == colored('A\n', 'blue', attrs=['bold'])


def test_space_separated_attrs():
    assert C('A', c=None, a='bold underline') == colored('A\n', attrs=['bold', 'underline'])


def test_space_separated_short_attrs():
    assert C('A', c=None, a='b u') == colored('A\n', attrs=['bold', 'underline'])


def test_mixed_shortcuts_and_full_attrs():
    assert C('A', c=None, a='b underline') == colored('A\n', attrs=['bold', 'underline'])


def test_double_attrs():
    assert C('A', c=None, a='b b') == colored('A\n', attrs=['bold'])


def test_all():
    attrs = ['blink', 'concealed']

    assert C(1, [], None, sep='|', end='.', c='blue', b='green', a=attrs) == \
        colored('1|[]|None.', 'blue', 'on_green', attrs)

    assert C(1, [], None, sep='|', end='.', c='b', b='g', a='blink c') == \
        colored('1|[]|None.', 'blue', 'on_green', attrs)
