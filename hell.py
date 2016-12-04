import inspect
import pprint
import sys

import termcolor


__author__ = 'Constantine Parkhimovich'
__copyright__ = 'Copyright 2016 Constantine Parkhimovich'
__license__ = 'MIT'
__title__ = 'hell'
__version__ = '0.2.1'

__all__ = ['Config', 'C', 'F', 'P', 'PP']


COLOR_SHORTCUTS = {
    'b': 'blue',
    'c': 'cyan',
    'g': 'green',
    # Threre is no shortcut for 'grey'
    'm': 'magenta',
    'r': 'red',
    'w': 'white',
    'y': 'yellow'
}

ATTR_SHORTCUTS = {
    'b': 'bold',
    # Threre is no shortcut for 'blink'
    'c': 'concealed',
    'd': 'dark',
    'r': 'reverse',
    'u': 'underline'
}


class Config:
    # Default color of C() output.
    C_DEFAULT_COLOR = 'green'
    # Format string used in F()
    F_TEMPLATE = '--> {filename} line {lineno} {funcname}()'
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
        red, green, blue, cyan, magenta, yellow, white, grey.

    Available background colors:
        red, green, yellow, blue, magenta, cyan, white.
    It is possible to use termcolor-like variants:
        on_red, on_green etc.

    color and background color can be passed as single letters:
        r, g, b, c, m, y, w. grey has no shortcut.

    Available attributes:
        bold, concealed, dark, reverse, underline, blink.
    Single letters can be passed as shortcuts:
        b, c, d, r, u. blink has no shortcut.
    Single attribute can be passed as string,
        multiple attributes should be passed as list of strings.
    """

    if c is not None:
        if len(c) == 1:
            c = COLOR_SHORTCUTS[c]
        if c == 'C_DEFAULT_COLOR':
            c = Config.C_DEFAULT_COLOR
 
    if b is not None:
        if len(b) == 1:
            b = COLOR_SHORTCUTS[b]
        if not b.startswith('on_'):
            b = 'on_' + b
 
    if isinstance(a, str):
        a = [a]
    if a is not None:
        a = [ATTR_SHORTCUTS[attr] if len(attr) == 1 else attr for attr in a]

    text = print_to_str(*args, sep=sep, end=end)

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


def F(frame=None, c=None, b=None, a=None):
    """
    "Where am I?"

    Print info about stack frame.

    If frame is not provided, frame called F() will be used.

    Info includes:
        python filename
        line number
        name of function that called F.
        name of type if function is its method or classmethod

    Info is being formatted using Config.F_TEMPLATE

    c, b, a are optional termcolor related arguments.
    See docstring of C() for details.

    Example usage:

    class Class:
        def function(self):
            F()

    Will print '/path/to/module.py line 114 Class.function()'

    """
    if frame is None:
        frame = inspect.currentframe().f_back

    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    funcname = frame.f_code.co_name

    # Caller function could actually be a method of some object.
    # If so, the first argument is that object.
    obj = None
    argvalues = inspect.getargvalues(frame)
    if argvalues.args:
        first_arg = argvalues.locals[argvalues.args[0]]
    elif argvalues.varargs:
        varargs = argvalues.locals[argvalues.varargs]
        if varargs:
            first_arg = varargs[0]
        else:
            first_arg = None
    else:
        first_arg = None

    if first_arg is not None:
        try:
            fn = inspect.getattr_static(first_arg, funcname)
        except AttributeError:
            fn = None
        else:
            # Caller is likely a method, or classmethod, or descriptor.
            # Check its code to make sure.
            fn = inspect.unwrap(fn)
            if isinstance(fn, (classmethod)) or funcname == '__new__':
                fn = getattr(fn, '__func__', None)
            elif isinstance(fn, property):
                fn = getattr(fn, 'fget', None)
            fn = inspect.unwrap(fn)
            funcname = getattr(fn, '__qualname__', funcname)
            assert not hasattr(fn, '__func__')
            f_code = getattr(fn, '__code__', None)
            if f_code is frame.f_code:
                obj = first_arg

    kwargs = {
        'filename': filename,
        'lineno': lineno,
        'funcname': funcname,
    }
    text = Config.F_TEMPLATE.format(**kwargs)

    C(text, c=c, b=b, a=a)

