hell
====
When you've got to debug your code.


## Installing
```bash
pip install hell
```

### Requirements
- python >= 3.10
- [termcolor](https://pypi.org/project/termcolor/)


## Usage
There is a collection of functions with short uppercase names. \
Most of them print colorized formatted output. \
Most of them accept short keyword arguments as options.

### Colors
- `black`
- `grey`  (Actually black but kept for backwards compatibility)
- `red`
- `green`
- `yellow`
- `blue`
- `magenta`
- `cyan`
- `light_grey`
- `dark_grey`
- `light_red`
- `light_green`
- `light_yellow`
- `light_blue`
- `light_magenta`
- `light_cyan`
- `white`

The first letters are shortcuts for colors:
`r`, `g`, `b`, `c`, `m`, `y`, `w` . grey has no shortcut.

### Attributes
+ bold
+ concealed
+ dark
+ reverse
+ underline
+ blink

The first letters can be used as well:
`b`, `c`, `d`, `r`, `u`. blink has no shortcut.


### Configuration
There is a `Config` class to adjust hell. Options are:

| option            | default      | description                                      |
| ----------------- | ------------ | ------------------------------------------------ |
| `C_DEFAULT_COLOR` | `'green'`    | Default color of C() output                      |
| `F_TEMPLATE`      | `'--> {filename} line {lineno} {funcname}()'`    | Format string used in F() |
| `OUT`             | `sys.stdout` | Writable file-like object to redirect output to. |

Example configuration change:
```python
import hell
hell.Config.OUT = open('/tmp/debug.out', 'a')
```


## Functions

- [C](#c)
- [F](#f)
- [I](#i)
- [L](#l)
- [M](#m)
- [P](#p)
- [PP](#pp)
- [T](#t)


## C

**C**(`*args`, _sep_=`' '`, _end_=`'\n'`, _c_=`C_DEFAULT_COLOR`, _b_=`None`, _a_=`None`)

Print _args_, colorized and formatted according to kwargs.

| kwarg | description      | default                  |
| ----- | ---------------- | ------------------------ |
| c     | color            | `Config.C_DEFAULT_COLOR` |
| b     | background color |
| a     | attributes, str like 'bold' or 'b u' or list of strings like ['bold', 'underline'] |
| sep   | separator, same as in built-in print                                      |
| end   | end, same as in built-in print                                            |

Examples:
```python
from hell import C
C('Some', 'variables')
C('debug note', c='yellow', b='white', a='underline')
C('shortcuts', c='y', b='w', a='u') # yellow underlined on white
C('multiple attributes', a=['bold', 'underline'])
C('multiple attributes as space-delimited string', a='bold underline')
C('multiple attributes as space-delimited string with shortcuts', a='b u')
C(123, 456, sep='|', end='.')
```


## F

**F**(_frame_=`None`, _c_=`None`, _b_=`None`, _a_=`None`, _depth_=`1`)

_"Where am I?"_

Print info about stack frame.

If _frame_ is not provided, frame called F() will be used.

Info includes:
- python filename
- line number
- name of function that called `F`.
- name of type if function is its method or classmethod

Info is being formatted using `Config.F_TEMPLATE`

_depth_ is to control number of stack frames to inspect.
E.g. `depth=2` is to print info on the function calling `F` and its caller.

_c_, _b_, _a_ are optional termcolor related arguments.
See [C](#c) for details.

Example usage:

```python
class Class:
    def function(self):
        F() # E.g. this lineno is 114
```
Will print:
```
/path/to/module.py line 114 Class.function()
```


## I

**I**(_banner_=`''`, _ipython_=`True`, _call\_f_=`True`, _c_=`None`, _b_=`None`, _a_=`None`)

Emulate interactive Python console.

Current locals and globals will be available.

_banner_ will be printed before first interaction. <br />
_banner=None_ is for printing default console banner. <br />
See built-in code.InteractiveConsole.interact.

_ipython=True_ indicates using IPython console if available.

When _call\_f_ is true, F() will be called printing info where I() was called.

_c_, _b_, _a_ are optional termcolor related arguments.
See [C](#c) for details.



## L

**L**(_sized_, _c_=`None`, _b_=`None`, _a_=`None`)

Print the length of _sized_, colorized and formatted according to keyword arguments.

_c_, _b_, _a_ are optional termcolor related arguments.
See [C](#c) for details.

```python
L('abc', c='b', a='underline')
```

Returns length with "pipe":
```python
>>> 'abc' | L
3
```


## M

**M**(_obj_, _c_=`None`, _b_=`None`, _a_=`None`, _sep_=`' | '`)

Print the base classes of type of the _obj_, \
or of the _obj_ itself when it is a type.

Bases will be in Method Resolution Order, \
separated with _sep_, \
colorized and formatted according to keyword arguments.

_c_, _b_, _a_ are optional termcolor related arguments.
See [C](#c) for details.


## P

**P**(`*args`, _sep_=`' '`, _end_=`'\n'`)

Shortcut for built-in function _print_ writing to `Config.OUT`


## PP

**PP**(_obj_, _indent_=`4`, _width_=`80`, _depth_=`None`, _compact_=`False`, _c_=`None`, _b_=`None`, _a_=`None`)

Pretty-print colorized python object.

| kwarg   | description                                          | default |
| ------- | ---------------------------------------------------- | ------- |
| indent  | amount of indentation added for each recursive level | 4
| width   | desired output width                                 | 80
| depth   | number of levels which may be printed                | not limited
| compact<br />(python3)| format as many items as will fit within the width<br /> on each output line | False
| c       | text color, see function [C](#c)                     | None
| b       | background color, see function [C](#c)               | None
| a       | attributes, see function [C](#c)                     | None

```python
from hell import PP
numbers = list(range(10))
PP(numbers, indent=4, width=15, compact=True)
```
will print
```
[   0, 1, 2, 3, 4,
    5, 6, 7, 8, 9,
        10, 11]
```


## T

**T**(_obj_, _c_=`None`, _b_=`None`, _a_=`None`)

Print the type of _obj_, colorized and formatted according to keyword arguments.

_c_, _b_, _a_ are optional termcolor related arguments.
See [C](#c) for details.

```python
T(0, c='r', a='bold')
```

Returns type with "pipe":
```python
>>> 123 | T
<class 'int'>
```

# Contributing
[Read here](https://github.com/blackelk/hell/blob/main/Contributing.md)
