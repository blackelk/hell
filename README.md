hell
====
Relieves pain of debug.


## Installing
```bash
pip install hell
```

### Requirements
**python 3.4+**

[termcolor](https://pypi.python.org/pypi/termcolor)


## Usage
In hell there is a collection of functions with short uppercase names. Most of them print colorized formatted output. Most of them accept short keyword arguments as options.

### Colors
+ blue
+ cyan
+ green (default)
+ grey
+ magenta
+ red
+ white
+ yellow

### Attributes
+ blink
+ bold
+ concealed
+ dark
+ reverse
+ underline

### Configuration
There is Config class to adjust hell. Options are:

| option            | default    | description                                      |
| ----------------- | ---------- | ------------------------------------------------ |
| C\_DEFAULT\_COLOR | 'green'    | Default color of C() output                      |
| OUT               | sys.stdout | Writable file-like object to redirect output to. |

Example configuration change:
```python
import hell
hell.Config.OUT = open('/tmp/debug.out', 'a')
```


## Tools


### C(\*args, sep=' ', end='\\n', c='C\_DEFAULT\_COLOR', b=None, a=None)

Print colorized *args*, colorized and formatted according to kwargs.

| kwarg | description      | default             |
| ----- | ---------------- | ------------------- |
| c     | color            | 'C\_DEFAULT\_COLOR' |
| b     | background color |
| a     | attributes, str like 'bold' or list of strings like ['bold', 'underline'] |
| sep   | separator, same as in built-in print                                      |
| end   | end, same as in built-in print                                            |

Examples:
```python
from hell import C
C('Some', 'variables')
C('debug note', c='yellow', b='white', a='underline')
C(123, 456, sep='|', end='.')
```


----
### P(\*args, sep=' ', end='\\n')
Shortcut for built-in function **print** writing to Config.OUT


----
### PP(obj, indent=4, width=80, depth=None, compact=False, c=None, b=None, a=None)
Pretty-print colorized python object.

| kwarg   | description                                          | default |
| ------- | ---------------------------------------------------- | ------- |
| indent  | amount of indentation added for each recursive level | 4
| width   | desired output width                                 | 80
| depth   | number of levels which may be printed                | not limited
| compact | format as many items as will fit within the width <br /> on each output line | False
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

