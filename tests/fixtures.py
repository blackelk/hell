from functools import wraps

from hell import F


def decorator(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper


def fn0():
    F()

def fn1(a):
    F()

def fn2(k1=1, k2=1):
    F()

@decorator
def fn3():
    F()

def gen1():
    F()
    yield 0


la1 = lambda : F()

la2 = lambda x: F()


class Descriptor:

    def __get__(self, instance, owner):
        F()

    def __set__(self, instance, value):
        F()


class Class:

    descriptor = Descriptor()

    def fn1(self):
        F()

    def fn2(zzz, aaa):
        F()

    def fn3(*a):
        F()

    @classmethod
    def fn4(cls):
        F()

    @staticmethod
    def fn5():
        F()

    @property
    def fn6(self):
        F()

    @decorator
    @decorator
    def fn7(self):
        F()

    @classmethod
    @decorator
    def fn8(self):
        F()

    def gen2(self):
        F()
        yield 0


class Class2:
    def __new__(cls):
        F()
        return object.__new__(cls)


class MetaClass(type):

    def __init__(self, *a):
        F()

    def __add__(cls, other):
        F()
        return Ellipsis

    @property
    def prop(cls):
        F()


class C1:

    def fn1(self):
        F()

    def fn2(self):
        F()

class C2(C1):

    def fn2(self):
        F()

    def fn3(self):
        F()


def fn0_depth2():
    F(depth=2)

def fn1_depth2():
    fn0_depth2()

def fn2_depth2():
    fn1_depth2()
