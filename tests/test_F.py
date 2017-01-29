from io import StringIO

from termcolor import colored

import fixtures as fix
from hell import Config, F


Config.OUT = StringIO()


def _test_F(lineno, funcname, func, f_args=(), f_kwargs=None):
    """
    Call func(*f_args, **kwargs)
    Read Config.OUT
    Assert it has module file, lineno and funcname formatted using Config.F_TEMPLATE.
    """
    if f_kwargs is None:
        f_kwargs = {}

    pos = Config.OUT.tell()
    func(*f_args, **f_kwargs)
    Config.OUT.seek(pos)

    kwargs = {
        'filename': fix.__file__,
        'lineno': lineno,
        'funcname': funcname
    }
    expected_out = colored(Config.F_TEMPLATE.format(**kwargs) + '\n')

    assert expected_out == Config.OUT.read()


def test_functions():

    _test_F(14, 'fn0', fix.fn0)

    _test_F(17, 'fn1', fix.fn1, (0,))

    _test_F(20, 'fn2', fix.fn2)

    g = fix.gen1()
    _test_F(27, 'gen1', next, (g,))


def test_methods():

    c = fix.Class()

    c.fn1()
    _test_F(50, 'Class.fn1', c.fn1)

    _test_F(53, 'Class.fn2', c.fn2, (0,))

    _test_F(56, 'Class.fn3', c.fn3)

    _test_F(60, 'Class.fn4', c.fn4)

    _test_F(64, 'fn5', c.fn5)

    _test_F(68, 'Class.fn6', lambda : c.fn6)

    _test_F(39, 'Descriptor.__get__', lambda : c.descriptor)

    def _set():
        c.descriptor = 0
    _test_F(42, 'Descriptor.__set__', _set)

    _test_F(73, 'Class.fn7', c.fn7)

    g = c.gen2()
    _test_F(81, 'Class.gen2', next, (g,))

    _test_F(87, 'Class2.__new__', fix.Class2)


def test_lambda():

    _test_F(31, '<lambda>', fix.la1)

    _test_F(33, '<lambda>', fix.la2, (0,))


def test_wrapper_descriptor():

    fix.Class3 = fix.MetaClass('Class3', (), {})
    _test_F(95, 'object.__init__', fix.MetaClass, ('Class3', (), {}))

    _test_F(98, 'MetaClass.__add__', lambda: (fix.Class3 + 1))

    _test_F(103, 'MetaClass.prop', lambda: fix.Class3.prop)


def test_inheritance():

    c2 = fix.C2()

    _test_F(109, 'C1.fn1', c2.fn1)

    _test_F(117, 'C2.fn2', c2.fn2)

    _test_F(120, 'C2.fn3', c2.fn3)

