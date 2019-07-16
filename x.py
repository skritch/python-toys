"""
Let's just call this documentation for magic method signatures, OK?
( https://docs.python.org/3/reference/datamodel.html#specialnames )

And don't get cocky, kid. https://docs.python.org/3/reference/datamodel.html#special-lookup

>>> from x import x
>>> list(map(x**2, [1, 2, 3]))
[1, 4, 9]
>>> list(map(x.pop, [[1, 2], [3, 4]]))
[2, 4]
"""


class Slot(object):
    __instance = None

    def __new__(cls):
        if Slot.__instance is None:
            Slot.__instance = object.__new__(cls)
        return Slot.__instance

__ = Slot()


def partial_if_slot(func, *args, **kwargs):
    for i, a in enumerate(args):
        if a is __:
            return lambda last_arg: func(*args[:i], last_arg, *args[i:], **kwargs)
    for k, v in kwargs.items():
        if v is __:
            kwargs.pop(k, None)
            return lambda last_kwarg: func(*args, **kwargs, k=last_kwarg)
    return func(*args, **kwargs)


def getattr_and_maybe_call(i, name):
    attr = getattr(i, name)
    if hasattr(attr, '__call__'):
        return attr.__call__()
    else:
        return attr


class X(object):
    __instance = None

    def __new__(cls):
        if X.__instance is None:
            X.__instance = object.__new__(cls)
        return X.__instance

    def __getattr__(self, name):
        # Any way to distinguish between an immediate and a deferred call?
        return lambda i: getattr_and_maybe_call(i, name)

    # --- nothing below this line is interesting ---

    def __call__(self, *args, **kwargs):
        return lambda i: i.__call__(*args, **kwargs)

    def __repr__(self):
        return lambda i: i.__repr__()

    def __str__(self):
        return lambda i: i.__str__()

    def __bytes__(self):
        return lambda i: i.__bytes__()

    def __format__(self, format_spec):
        return lambda i: i.__format__(format_spec)

    def __lt__(self, other):
        return lambda i: i.__lt__(other)

    def __le__(self, other):
        return lambda i: i.__le__(other)

    def __eq__(self, other):
        return lambda i: i.__eq__(other)

    def __ne__(self, other):
        return lambda i: i.__ne__(other)

    def __gt__(self, other):
        return lambda i: i.__gt__(other)

    def __ge__(self, other):
        return lambda i: i.__ge__(other)

    def __hash__(self):
        return lambda i: i.__hash__()

    def __bool__(self):
        return lambda i: i.__bool__()

    def __dir__(self):
        return lambda i: i.__dir__()

    def __len__(self):
        return lambda i: i.__len__()

    def __getitem__(self, key):
        return lambda i: i.__getitem__(key)

    def __iter__(self):
        return lambda i: i.__iter__()

    def __reversed__(self):
        return lambda i: i.__reversed__()

    def __contains__(self, item):
        return lambda i: i.__contains__(item)

    def __add__(self, other):
        return lambda i: i.__add__(other)

    def __sub__(self, other):
        return lambda i: i.__sub__(other)

    def __mul__(self, other):
        return lambda i: i.__mul__(other)

    def __matmul__(self, other):
        return lambda i: i.__matmul__(other)

    def __truediv__(self, other):
        return lambda i: i.__truediv__(other)

    def __floordiv__(self, other):
        return lambda i: i.__floordiv__(other)

    def __mod__(self, other):
        return lambda i: i.__mod__(other)

    def __divmod__(self, other):
        return lambda i: i.__divmod__(other)

    def __pow__(self, other, modulo=None):
        return lambda i: i.__pow__(other, modulo)

    def __lshift__(self, other):
        return lambda i: i.__lshift__(other)

    def __rshift__(self, other):
        return lambda i: i.__rshift__(other)

    def __and__(self, other):
        return lambda i: i.__and__(other)

    def __xor__(self, other):
        return lambda i: i.__xor__(other)

    def __or__(self, other):
        return lambda i: i.__or__(other)

    def __radd__(self, other):
        return lambda i: i.__radd__(other)

    def __rsub__(self, other):
        return lambda i: i.__rsub__(other)

    def __rmul__(self, other):
        return lambda i: i.__rmul__(other)

    def __rmatmul__(self, other):
        return lambda i: i.__rmatmul__(other)

    def __rtruediv__(self, other):
        return lambda i: i.__rtruediv__(other)

    def __rfloordiv__(self, other):
        return lambda i: i.__rfloordiv__(other)

    def __rmod__(self, other):
        return lambda i: i.__rmod__(other)

    def __rdivmod__(self, other):
        return lambda i: i.__rdivmod__(other)

    def __rpow__(self, other):
        return lambda i: i.__rpow__(other)

    def __rlshift__(self, other):
        return lambda i: i.__rlshift__(other)

    def __rrshift__(self, other):
        return lambda i: i.__rrshift__(other)

    def __rand__(self, other):
        return lambda i: i.__rand__(other)

    def __rxor__(self, other):
        return lambda i: i.__rxor__(other)

    def __ror__(self, other):
        return lambda i: i.__ror__(other)

    def __iadd__(self, other):
        return lambda i: i.__iadd__(other)

    def __isub__(self, other):
        return lambda i: i.__isub__(other)

    def __imul__(self, other):
        return lambda i: i.__imul__(other)

    def __imatmul__(self, other):
        return lambda i: i.__imatmul__(other)

    def __itruediv__(self, other):
        return lambda i: i.__itruediv__(other)

    def __ifloordiv__(self, other):
        return lambda i: i.__ifloordiv__(other)

    def __imod__(self, other):
        return lambda i: i.__imod__(other)

    def __ipow__(self, other, modulo=None):
        return lambda i: i.__ipow__(other, modulo)

    def __ilshift__(self, other):
        return lambda i: i.__ilshift__(other)

    def __irshift__(self, other):
        return lambda i: i.__irshift__(other)

    def __iand__(self, other):
        return lambda i: i.__iand__(other)

    def __ixor__(self, other):
        return lambda i: i.__ixor__(other)

    def __ior__(self, other):
        return lambda i: i.__ior__(other)

    def __pos__(self):
        return lambda i: i.__pos__()

    def __abs__(self):
        return lambda i: i.__abs__()

    def __invert__(self):
        return lambda i: i.__invert__()

    def __complex__(self):
        return lambda i: i.__complex__()

    def __int__(self):
        return lambda i: i.__int__()

    def __float__(self):
        return lambda i: i.__float__()

    def __round__(self, n=None):
        return lambda i: i.__round__(n)

    def __index__(self):
        return lambda i: i.__index__()


x = X()
