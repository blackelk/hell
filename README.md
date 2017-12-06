hell
====
When you've got to debug your code.


## Installing
```bash
pip install hell
```

### Requirements
hell supports **python 3.4+** and **2.7**

[termcolor](https://pypi.python.org/pypi/termcolor)


## Usage
In hell there is a collection of functions with short uppercase names. Most of them print colorized formatted output. Most of them accept short keyword arguments as options.

### Colors
+ red
+ green (default)
+ blue
+ cyan
+ magenta
+ yellow
+ white
+ grey

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
There is `Config` class to adjust hell. Options are:

| option            | default    | description                                      |
| ----------------- | ---------- | ------------------------------------------------ |
| C\_DEFAULT\_COLOR | 'green'    | Default color of C() output                      |
| F\_TEMPLATE       | '--> {filename} line {lineno} {funcname}()'    | Format string used in F() |
| OUT               | sys.stdout | Writable file-like object to redirect output to. |

Example configuration change:
```python
import hell
hell.Config.OUT = open('/tmp/debug.out', 'a')
```


## Tools


**C**(\*_args_, _sep=' '_, _end='\\n'_, _c='C\_DEFAULT\_COLOR'_, _b=None_, _a=None_)

Print _args_, colorized and formatted according to kwargs.

| kwarg | description      | default             |
| ----- | ---------------- | ------------------- |
| c     | color            | 'C\_DEFAULT\_COLOR' |
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


<br />

- - - -
**F**(_frame=None_, _c=None_, _b=None_, _a=None_)

_"Where am I?"_

Print info about stack frame.

If _frame_ is not provided, frame called F() will be used.

Info includes:
- python filename
- line number
- name of function that called F.
- name of type if function is its method or classmethod

Info is being formatted using `Config.F_TEMPLATE`

_c_, _b_, _a_ are optional termcolor related arguments.
See C() for details.

Example usage:

```python
class Class:
    def function(self):
        F()
```
Will print:
```
/path/to/module.py line 105 Class.function()
```


<br />

- - - -
**I**(_banner=''_, _ipython=True_, _call\_f=True_,_c=None_, _b=None_, _a=None_)

Emulate interactive Python console.

Current locals and globals will be available.

_banner_ will be printed before first interaction. <br />
_banner=None_ is for printing default console banner. <br />
See built-in code.InteractiveConsole.interact.

_ipython=True_ indicates using IPython console if available.

When _call\_f_ is true, F() will be called printing info where I() was called.

_c_, _b_, _a_ are optional termcolor related arguments.
See C() for details.


<br />

- - - -
**L**(_s_, _c=None_, _b=None_, _a=None_)

Print the length of _s_, colorized and formatted according to keyword arguments.

_c_, _b_, _a_ are optional termcolor related arguments.
See C() for details.


<br />

- - - -
**P**(\*_args_, _sep=' '_, _end='\\n'_)

Shortcut for built-in function _print_ writing to `Config.OUT`


<br />

- - - -
**PP**(_obj_, _indent=4_, _width=80_, _depth=None_, _compact=False_, _c=None_, _b=None_, _a=None_)

Pretty-print colorized python object.

| kwarg   | description                                          | default |
| ------- | ---------------------------------------------------- | ------- |
| indent  | amount of indentation added for each recursive level | 4
| width   | desired output width                                 | 80
| depth   | number of levels which may be printed                | not limited
| compact<br />(python3)| format as many items as will fit within the width<br /> on each output line | False
| c       | text color, see function C                           | None
| b       | background color, see function C                     | None
| a       | attributes, see function C                           | None

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

