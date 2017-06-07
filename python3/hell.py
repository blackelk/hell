import code
import inspect
import pprint
import sys

import termcolor

try:
    import readline
except ImportError:
    readline = None
else:
    import rlcompleter


__author__ = 'Constantine Parkhimovich'
__copyright__ = 'Copyright 2016-2017 Constantine Parkhimovich'
__license__ = 'MIT'
__title__ = 'hell'
__version__ = '0.3.1'

__all__ = ['Config', 'C', 'F', 'I', 'P', 'PP']


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
    Single attribute can be passed as string:
        C(123, a='underline')
    multiple attributes can be passed as space-delimited string
        or list of strings:
        C(456, a='underline bold')
        C(789, a=['underline', 'b'])
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
        a = a.split()
    if a is not None:
        a = [ATTR_SHORTCUTS[attr] if len(attr) == 1 else attr for attr in a]
        # Unique attrs, preserve order.
        a_unique = set()
        a = [attr for attr in a if not(attr in a_unique or a_unique.add(attr))]

    text = print_to_str(*args, sep=sep, end=end)

    text = termcolor.colored(text, color=c, on_color=b, attrs=a)

    Config.OUT.write(text)


def PP(obj, indent=4, width=80, depth=None, *, compact=False, c=None, b=None, a=None):
    """
    Pretty-print colorized python object.

    indent      amount of indentation added for each recursive level
    depth       number of levels which may be printed
    width       desired output width
    compact     format as many items as will fit within the width
                on each output line
    c, b, a     see C().
    """
    text = pprint.pformat(obj, indent, width, depth, compact=compact)
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
    #obj = None
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
            if isinstance(fn, classmethod) or funcname == '__new__':
                fn = getattr(fn, '__func__', None)
            elif isinstance(fn, property):
                fn = getattr(fn, 'fget', None)
            fn = inspect.unwrap(fn)
            assert not hasattr(fn, '__func__')
            funcname = getattr(fn, '__qualname__', funcname)
            #f_code = getattr(fn, '__code__', None)
            #if f_code is frame.f_code:
            #    obj = first_arg

    kwargs = {
        'filename': filename,
        'lineno': lineno,
        'funcname': funcname,
    }
    text = Config.F_TEMPLATE.format(**kwargs)

    C(text, c=c, b=b, a=a)


def I(banner='', *, ipython=True, call_f=True, c=None, b=None, a=None):
    """
    Emulate interactive Python console.

    Current locals and globals will be available.

    banner will be printed before first interaction.
    banner=None is for printing default console banner.
    See built-in code.InteractiveConsole.interact.

    ipython=True indicates using IPython console if available.

    When call_f is true, F() will be called printing info where I() was called.

    c, b, a are optional termcolor related arguments.
    """

    frame = inspect.currentframe().f_back

    ns = frame.f_globals.copy()
    ns.update(frame.f_locals)

    if readline:
        readline.parse_and_bind('tab: complete')

    if call_f:
        F(frame, c=c, b=b, a=a)

    if banner:
        C(banner, c=c, b=b, a=a)

    if ipython:
        try:
            import IPython
        except ImportError:
            ipython = False

    if ipython:
        func = IPython.embed
        kwargs = {
            'confirm_exit': False,
            'user_ns': ns
        }
        if banner is not None:
            kwargs['display_banner'] = False
    else:
        func = code.interact
        kwargs = {'local': ns}
        if banner is not None:
            kwargs['banner'] = ''

    func(**kwargs)

