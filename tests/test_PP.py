from pprint import pformat

from termcolor import colored

from hell import PP as PP_orig
from tests.capture_out import capture_out


PP = capture_out(PP_orig)

mars = {
    'name': 'Mars',
    'mass': 6.4171e+23,
    'radius': 3389.5,
    'satellites': [
        {
            'name': 'Phobos',
            'mass': 1.0659e+16,
            'radius': 11.2667
        },
        {
            'name': 'Deimos',
            'mass': 1.4762e+15,
            'radius': 6.2
        }
    ],
}

numbers = list(range(100))


def _pformat(*args, **kwargs):
    return pformat(*args, **kwargs) + '\n'


def test_scalar():
    assert PP('') == colored("''\n")
    assert PP(None) == colored('None\n')


def test_indent():
    assert PP(mars, indent=1) == colored(_pformat(mars, indent=1))
    assert PP(mars) == colored(_pformat(mars, indent=4))


def test_width():
    assert PP(mars, width=10) == colored(_pformat(mars, indent=4, width=10))
    assert PP(mars) == colored(_pformat(mars, indent=4, width=80))


def test_depth():
    assert PP(mars, depth=2) == colored(_pformat(mars, indent=4, depth=2))
    assert PP(mars) == colored(_pformat(mars, indent=4, depth=None))


def test_compact():
    assert PP(numbers, indent=2, compact=True) == \
        colored(_pformat(numbers, indent=2, compact=True))

    assert PP(numbers, indent=2) == \
        colored(_pformat(numbers, indent=2, compact=False))


def test_c():
    assert PP(mars, c='green') == colored(_pformat(mars, indent=4), 'green')
    assert PP(mars, c='g') == colored(_pformat(mars, indent=4), 'green')


def test_b():
    assert PP(mars, b='red') == colored(_pformat(mars, indent=4), on_color='on_red')
    assert PP(mars, b='on_red') == colored(_pformat(mars, indent=4), on_color='on_red')
    assert PP(mars, b='r') == colored(_pformat(mars, indent=4), on_color='on_red')


def test_a():
    underlined_mars = colored(_pformat(mars, indent=4), attrs=['underline'])

    assert PP(mars, a=['underline']) == underlined_mars
    assert PP(mars, a='underline') == underlined_mars
    assert PP(mars, a='u') == underlined_mars
    assert PP(mars, a=['u']) == underlined_mars

    assert PP(1, a='bold reverse') == colored(_pformat(1), attrs=['bold', 'reverse'])
    assert PP(1, a='b r') == colored(_pformat(1), attrs=['bold', 'reverse'])


def test_all():
    attrs = ['bold', 'underline']
    kwargs = dict(indent=4, width=10, depth=2)

    assert PP(mars, c='blue', b='red', a=attrs, **kwargs) == \
        colored(_pformat(mars, **kwargs), color='blue', on_color='on_red',
                attrs=attrs)
