"""
`python3 -m doctest -v mapped.py`

TODO:
- Concoct a nice way to pipe into functions taking multiple arguments.
- Note precisely python's order of operations.
- Rearrange tracebacks that go through the mapped object so that they're informative.
- Also, the __repr__ should give information about the original operations, not a list of lambdas.
- Maybe mangle method names if there are collisions.
- Provide a nice way to do batched operations on a mapped iterable,
    or to re-arrange a mapped iterable by keys (a better groupby)
- Overload other magic methods for fun, profit.
- Consider whether there's a better approach to handling iterator arguments than
    leaving up to the caller (but I don't think so). At least provide an example of batching something that
    is prohibitively large to keep in memory (either along with `list()` or `tee()`).
- setdefault and other mutating methods?
- Make compatible with python 2 or 3
"""

from functools import reduce


class Mapped(object):
    def __init__(self, iterable, steps=None):
        """
        Construct an iterator that lazily maps attr / index / key lookups across the provided iterable,
        and allows "piping" into single argument functions.
        To evaluate the mapped functions, wrap it in `list()` or `iter()`.
        Each operation generates a new Mapped, allowing branching (doesn't work on actual iterators, though).

        Ex:
        >>> import json
        >>> from math import sqrt
        >>> obj = [{'x': [{'y': {'z': 25} }] }, {'x': [{'y': {'z': 36 } }] }]
        >>> m = Mapped(obj)['x'][0]['y']
        >>> m1 = m | json.dumps
        >>> m2 = m['z'] | sqrt | int
        >>> list(m1)
        ['{"z": 25}', '{"z": 36}']
        >>> list(m2)
        [5, 6]

        If `iterable` is actually an iterator, branching the Mapped object won't work, as the underlying
        iterator will be exhausted the first time a Mapped is realized. Wrap the argument in `list()` or
        use `itertools.tee` to avoid this, Mapped isn't ready to do it for you. :)
        >>> r = Mapped(iter(range(4)))
        >>> list(r | (lambda x: x**2))
        [0, 1, 4, 9]
        >>> list(r | (lambda x: x**3))
        []

        """
        self._iterable = iterable
        self._steps = steps if steps else list()

    def _add_step(self, new_step):
        steps = list(self._steps) + [new_step]
        return Mapped(self._iterable, steps)

    @property
    def _all_steps(self):
        def identity(x):
            return x

        def compose(f, g):
            def composed(i):
                return g(f(i))
            return composed

        return reduce(
            compose,  # function composition
            self._steps,
            identity  # initializer
        )

    def __getattr__(self, name):
        """
        >>> from collections import namedtuple
        >>> Point = namedtuple('Point', ['x', 'y'])
        >>> points = Mapped([Point(1, 0), Point(2, 0)])
        >>> list(points.x)
        [1, 2]
        """

        def __getattr__(i):
            return getattr(i, name)
        return self._add_step(__getattr__)

    def __getitem__(self, key):
        """
        >>> list(Mapped([[1], [2]])[0])
        [1, 2]
        """
        def __getitem__(i):
            return i[key]
        return self._add_step(__getitem__)

    def _get(self, key, default=None):
        """
        Return self[key] if it exists, otherwise return `default`.

        >>> list(Mapped([{'a': 1}, {}])._get('a', 2))
        [1, 2]

        """
        def _get(i):
            return self._get_even_from_list(i, key, default)

        return self._add_step(_get)

    def __or__(self, f):
        """
        "Pipe" the Mapped iterator into `f`, adding x -> f(x) to the steps stack.

        >>> list(Mapped(['1', '2']) | int)
        [1, 2]
        """
        return self._add_step(f)

    def __call__(self, *args, **kwargs):
        """
        >>> list(Mapped([float, str])(2))
        [2.0, '2']

        TBD: I don't think *args, **kwargs is sufficient here.
        """
        def __call__(f):
            return f(*args, **kwargs)
        return self._add_step(__call__)

    @staticmethod
    def _get_even_from_list(obj, key, default=None):
        if isinstance(obj, dict):
            return obj.get(key, default)
        try:
            return obj[key]
        except IndexError:
            return default

    def __repr__(self):
        return "<{}({}) steps={}>".format(self.__class__.__name__, self._iterable, self._steps)

    def __iter__(self):
        """
        Convert the Mapped object to an iterator that applies all the steps, composed, to the Mapped's _iterable.
        A python2 implementation should use itertools.imap here.
        """
        return map(
            self._all_steps,
            self._iterable
        )

    def _maybe(self, default=None):
        """
        Wrap all steps so far in a try, returning default if they raise.

        >>> l = [{'x': [1]}, {}]
        >>> list(Mapped(l)['x'][0]._maybe(default=2))
        [1, 2]
        """
        def maybe_do_steps(x):
            try:
                return self._all_steps(x)
            except:
                return default
        return Mapped(self._iterable, [maybe_do_steps])






