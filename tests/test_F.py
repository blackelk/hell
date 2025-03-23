from io import StringIO

from termcolor import colored

import tests.fixtures as fix
from hell import Config, F



# Wrapping F with capture_out would be adding bias.
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

    _test_F(24, 'fn3', fix.fn3)

    g = fix.gen1()
    _test_F(27, 'gen1', next, (g,))


def test_methods():

    c = fix.Class()

    _test_F(50, 'Class.fn1', c.fn1)

    _test_F(53, 'Class.fn2', c.fn2, (0,))

    _test_F(56, 'Class.fn3', c.fn3)

    _test_F(60, 'Class.fn4', fix.Class.fn4)

    _test_F(64, 'fn5', c.fn5)

    _test_F(68, 'Class.fn6', lambda : c.fn6)

    _test_F(39, 'Descriptor.__get__', lambda : c.descriptor)

    def _set():
        c.descriptor = 0
    _test_F(42, 'Descriptor.__set__', _set)

    _test_F(73, 'Class.fn7', c.fn7)

    _test_F(78, 'Class.fn8', fix.Class.fn8)

    g = c.gen2()
    _test_F(81, 'Class.gen2', next, (g,))


def test__new__():
    _test_F(87, 'Class2.__new__', fix.Class2)


def test_lambda():

    _test_F(31, '<lambda>', fix.la1)

    _test_F(33, '<lambda>', fix.la2, (0,))


def test_wrapper_descriptors():

    _test_F(94, 'object.__init__', fix.MetaClass, ('Class3', (), {}))

    Class3 = fix.MetaClass('Class3', (), {})

    _test_F(97, 'MetaClass.__add__', lambda: (Class3 + 1))

    _test_F(102, 'MetaClass.prop', lambda: Class3.prop)


def test_inheritance():

    c2 = fix.C2()

    _test_F(108, 'C1.fn1', c2.fn1)

    _test_F(116, 'C2.fn2', c2.fn2)

    _test_F(119, 'C2.fn3', c2.fn3)

def test_depth_10():
    """Test F() with depth=10 to ensure it prints up to 10 levels of stack frames."""
    pos = Config.OUT.tell()
    F(depth=10)  # Call F() at the deepest level
    Config.OUT.seek(pos)
    # Read all 10 expected lines
    output_lines = Config.OUT.read().strip().split('\n')
    assert len(output_lines) == 10

def test_depth_2():
    pos = Config.OUT.tell()
    fix.fn2_depth2()
    Config.OUT.seek(pos)
    kwargs1 = {
        'filename': fix.__file__,
        'lineno': 126,
        'funcname': fix.fn1_depth2.__name__
    }
    kwargs2 = {
        'filename': fix.__file__,
        'lineno': 123,
        'funcname': fix.fn0_depth2.__name__
    }
    expected_line_1 = colored(Config.F_TEMPLATE.format(**kwargs1))
    expected_line_2 = colored(Config.F_TEMPLATE.format(**kwargs2))
    result_lines = Config.OUT.read().strip().split('\n')
    assert len(result_lines) == 2
    assert result_lines == [expected_line_1, expected_line_2]

def test_depth_0():
    """Test F() with depth=0 to ensure it prints only the current stack frame."""
    pos = Config.OUT.tell()
    F(depth=0)
    Config.OUT.seek(pos)
    output = Config.OUT.read().strip()
    assert output == ""
