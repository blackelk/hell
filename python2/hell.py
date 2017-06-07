from __future__ import print_function

import code
import inspect
import pprint
import sys
import types

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


########################### getattr_static ##################################

_sentinel = object()


def _static_getmro(klass):
    return type.__dict__['__mro__'].__get__(klass)


def _check_instance(obj, attr):
    instance_dict = {}
    try:
        instance_dict = object.__getattribute__(obj, "__dict__")
    except AttributeError:
        pass
    return dict.get(instance_dict, attr, _sentinel)


def _check_class(klass, attr):
    for entry in _static_getmro(klass):
        if _shadowed_dict(type(entry)) is _sentinel:
            try:
                return entry.__dict__[attr]
            except KeyError:
                pass
    return _sentinel


def _is_type(obj):
    try:
        _static_getmro(obj)
    except TypeError:
        return False
    return True


def _shadowed_dict(klass):
    dict_attr = type.__dict__["__dict__"]
    for entry in _static_getmro(klass):
        try:
            class_dict = dict_attr.__get__(entry)["__dict__"]
        except KeyError:
            pass
        else:
            if not (type(class_dict) is types.GetSetDescriptorType and
                    class_dict.__name__ == "__dict__" and
                    class_dict.__objclass__ is entry):
                return class_dict
    return _sentinel


def getattr_static(obj, attr, default=_sentinel):
    """Retrieve attributes without triggering dynamic lookup via the
       descriptor protocol,  __getattr__ or __getattribute__.

       Note: this function may not be able to retrieve all attributes
       that getattr can fetch (like dynamically created attributes)
       and may find attributes that getattr can't (like descriptors
       that raise AttributeError). It can also return descriptor objects
       instead of instance members in some cases. See the
       documentation for details.

    Backported from Python 3.5.2
    """
    instance_result = _sentinel
    if not _is_type(obj):
        klass = type(obj)
        dict_attr = _shadowed_dict(klass)
        if (dict_attr is _sentinel or
            type(dict_attr) is types.MemberDescriptorType):
            instance_result = _check_instance(obj, attr)
    else:
        klass = obj

    klass_result = _check_class(klass, attr)

    if instance_result is not _sentinel and klass_result is not _sentinel:
        if (_check_class(type(klass_result), '__get__') is not _sentinel and
            _check_class(type(klass_result), '__set__') is not _sentinel):
            return klass_result

    if instance_result is not _sentinel:
        return instance_result
    if klass_result is not _sentinel:
        return klass_result

    if obj is klass:
        # for types we check the metaclass too
        for entry in _static_getmro(type(klass)):
            if _shadowed_dict(type(entry)) is _sentinel:
                try:
                    return entry.__dict__[attr]
                except KeyError:
                    pass
    if default is not _sentinel:
        return default
    raise AttributeError(attr)


def _getattr_base_static(obj, attr):

    if isinstance(obj, type):
        for base in inspect.getmro(obj):
            if attr in base.__dict__:
                return base.__dict__[attr], base

    for base in inspect.getmro(type(obj)):
        if attr in base.__dict__:
            return base.__dict__[attr], base

    raise AttributeError(attr)


#############################################################################


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


def force_unicode(s):

    if isinstance(s, unicode):
        return s
    elif isinstance(s, str):
        return s.decode('utf-8')
    else:
        return unicode(s)


def P(*args, **kwargs):
    """
    Shortcut for built-in function print writing to Config.OUT.
    P(value, ..., sep=' ', end='\n')
    """
    sep = force_unicode(kwargs.get('sep', u' '))
    end = force_unicode(kwargs.get('end', u'\n'))

    for k in kwargs:
        if k not in {'sep', 'end'}:
            raise TypeError('{} is an invalid keyword argument for this function'.format(k))

    print(*[force_unicode(a) for a in args], sep=sep, end=end, file=Config.OUT)


def C(*args, **kwargs):
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

    sep = force_unicode(kwargs.get('sep', u' '))
    end = force_unicode(kwargs.get('end', u'\n'))
    c = kwargs.get('c', 'C_DEFAULT_COLOR')
    b = kwargs.get('b')
    a = kwargs.get('a')

    for k in kwargs:
        if k not in {'sep', 'end', 'c', 'b', 'a'}:
            raise TypeError('{} is an invalid keyword argument for this function'.format(k))

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

    text = sep.join([force_unicode(arg) for arg in args]) + end

    text = termcolor.colored(text, color=c, on_color=b, attrs=a)

    Config.OUT.write(text)


def PP(obj, indent=4, width=80, depth=None, c=None, b=None, a=None):
    """
    Pretty-print colorized python object.

    indent      amount of indentation added for each recursive level
    depth       number of levels which may be printed
    width       desired output width
    c, b, a     see C().
    """
    text = pprint.pformat(obj, indent, width, depth)
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

    # Caller function can actually be a method of some class/object - "owner".
    # If so, the first argument is the owner.
    owner = None
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
            fn, base = _getattr_base_static(first_arg, funcname)
        except AttributeError:
            fn = None
        else:
            # Caller is likely a method, or classmethod, or descriptor.
            # Check its code to make sure.
            if isinstance(fn, classmethod) or funcname == '__new__':
                fn = getattr_static(fn, '__func__', None)
            elif isinstance(fn, property):
                fn = getattr_static(fn, 'fget', None)
            assert not hasattr(fn, '__func__')

            try:
                f_code = object.__getattribute__(fn, '__code__')
            except AttributeError:
                pass
            else:
                if f_code is frame.f_code:
                    funcname = '{}.{}'.format(base.__name__, funcname)
                    owner = base

    kwargs = {
        'filename': filename,
        'lineno': lineno,
        'funcname': funcname,
        'owner': owner,
    }
    text = Config.F_TEMPLATE.format(**kwargs)

    C(text, c=c, b=b, a=a)


def I(banner='', ipython=True, call_f=True, c=None, b=None, a=None):
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
        C(banner, c=c, b=b, a=a, end='')

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

    print('.')
    func(**kwargs)

