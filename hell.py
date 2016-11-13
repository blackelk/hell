import pprint
import sys

import termcolor


__author__ = 'Constantine Parkhimovich'
__copyright__ = 'Copyright 2016 Constantine Parkhimovich'
__license__ = 'MIT'
__title__ = 'hell'
__version__ = '0.1.0'

__all__ = ['Config', 'C', 'P', 'PP']


class Config:
    # Default color of C() output.
    C_DEFAULT_COLOR = 'green'
    # Writable file-like object to redirect output to.
    OUT = sys.stdout


def print_to_str(*args, sep=' ', end='\n'):
    """Format args like built-in print function does."""
    return sep.join([str(a) for a in args]) + end


def P(*args, sep=' ', end='\n'):
    """Shortcut for built-in function print writing to Config.OUT."""
    print(*args, sep=sep, end=end, file=Config.OUT)


def C(*args, sep=' ', end='\n', c='C_DEFAULT_COLOR', b=None, a=None):
    """
    Print args, colorized and formatted according to keyword arguments.

    Format args like built-in print function does,
        then prints colorized output to Config.OUT.

    c is for color, b is for background, a is for attributes.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available background colors:
        red, green, yellow, blue, magenta, cyan, white.
    It is possible to use termcolor-like variants:
        on_red, on_green etc.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.
    Single attribute can be passed as string,
        multiple attributes should be passed as list of strings.
    """
    if c == 'C_DEFAULT_COLOR':
        c = Config.C_DEFAULT_COLOR
 
    text = print_to_str(*args, sep=sep, end=end)
 
    if isinstance(b, str) and not b.startswith('on_'):
        b = 'on_' + b
 
    if isinstance(a, str):
        a = [a]
 
    text = termcolor.colored(text, color=c, on_color=b, attrs=a)
    Config.OUT.write(text)


def PP(obj, indent=4, width=80, depth=None, compact=False, c=None, b=None, a=None):
    """
    Pretty-print colorized python object.

    indent      amount of indentation added for each recursive level
    depth       number of levels which may be printed
    width       desired output width
    compact     format as many items as will fit within the width
                on each output line
    c, b, a     see C().
    """
    text = pprint.pformat(obj, indent=indent, width=width, depth=depth,
                          compact=compact)
    C(text, c=c, b=b, a=a)

