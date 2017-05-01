from termcolor import colored

from hell import C, Config
from conftest import capture_out


c = capture_out(C)

default = Config.C_DEFAULT_COLOR


def test_args():

    assert c() == colored('\n', default)

    assert c('A') == colored('A\n', default)

    assert c(1) == colored('1\n', default)

    assert c(['a', 'b', 'c']) == colored("['a', 'b', 'c']\n", default)

    assert c(1, 2) == colored('1 2\n', default)


def test_sep_end():

    assert c(1, 2, sep='|') == colored('1|2\n', default)

    assert c(1, end='.') == colored('1.', default)

    assert c(1, sep='|', end='.') == colored('1.', default)


def test_c_none():

    assert c('A', c=None) == colored('A\n')


def test_c():

    assert c('A', c='white') == colored('A\n', 'white')


def test_b():

    assert c('A', c='yellow', b='green') == colored('A\n', 'yellow', 'on_green')


def test_on_b():

    assert c('A', c='magenta', b='on_green') == colored('A\n', 'magenta', 'on_green')


def test_a_str():

    assert c('A', c='grey', a='underline') == colored('A\n', 'grey', attrs=['underline'])


def test_a_list():

    assert c('A', c='cyan', a=['reverse']) == colored('A\n', 'cyan', attrs=['reverse'])

    assert c('A', c='red', a=['bold', 'dark']) == colored('A\n', 'red', attrs=['bold', 'dark'])


def test_shortcuts():

    assert c('A', c='b') == colored('A\n', 'blue')

    assert c('A', c='b', b='g') == colored('A\n', 'blue', 'on_green')

    assert c('A', c='b', a='b') == colored('A\n', 'blue', attrs=['bold'])


def test_space_separated_attrs():

    assert c('A', c=None, a='bold underline') == colored('A\n', attrs=['bold', 'underline'])


def test_space_separated_short_attrs():

    assert c('A', c=None, a='b u') == colored('A\n', attrs=['bold', 'underline'])


def test_mixed_shortcuts_and_full_attrs():

    assert c('A', c=None, a='b underline') == colored('A\n', attrs=['bold', 'underline'])


def test_double_attrs():

    assert c('A', c=None, a='b b') == colored('A\n', attrs=['bold'])


def test_all():

    attrs = ['blink', 'concealed']

    assert c(1, [], None, sep='|', end='.', c='blue', b='green', a=attrs) == \
        colored('1|[]|None.', 'blue', 'on_green', attrs)

    assert c(1, [], None, sep='|', end='.', c='b', b='g', a='blink c') == \
        colored('1|[]|None.', 'blue', 'on_green', attrs)

