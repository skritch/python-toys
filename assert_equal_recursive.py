import unittest
from itertools import zip_longest


class TestRecursive(unittest.TestCase):
    def assertEqualRecursive(self, first, second):
        """
        Asserts that two nested JSON-like structures consisting of dictionaries and lists are fully equal.


        >>> TestRecursive().assertEqualRecursive({1: [{'a': 2}, 'b']}, {1: [{'a': 3}, 'b']})
        Traceback (most recent call last):
        ...
        AssertionError:
        Values differ: 2 != 3 at [1][0][a]

        """
        paths = self._check_equal_recursive(first, second)
        if paths:
            msg = '\n' + '\n'.join(paths)
            raise self.failureException(msg)

    def _check_equal_recursive(self, first, second, *path_so_far):
        diffs = []
        if isinstance(first, list) and isinstance(second, list):
            for i, (f, s) in enumerate(zip_longest(first, second)):
                diffs.extend(
                    self._check_equal_recursive(f, s, str(i), *path_so_far)
                )
            return diffs

        joined_path = ']['.join(str(i) for i in reversed(path_so_far))
        if isinstance(first, dict) and isinstance(second, dict):
            keys1 = first.keys()
            keys2 = second.keys()
            for k in keys1 - keys2:
                diffs.append('`{k}: {v}` not found in second object at [{path}] '.format(
                    path=joined_path,
                    k=k,
                    v=first[k]
                ))
            for k in keys2 - keys1:
                diffs.append('`{k}: {v}` not found in first object at [{path}] '.format(
                    path=joined_path,
                    k=k,
                    v=second[k]
                ))
            for k in keys1 & keys2:
                diffs.extend(
                    self._check_equal_recursive(first[k], second[k], k, *path_so_far)
                )
        elif not first == second:
            # If one is still a dict or list, don't display (since it might be large),
            # and don't str() since it's a json type
            if {type(first), type(second)} & {dict, list}:
                diffs.append('Types differ: {first} != {second} at [{path}]'.format(
                    path=joined_path,
                    first=type(first),
                    second=type(second)
                ))
            # Also don't compare other json types as strings
            elif {type(first), type(second)} & {int, float, bool, type(None)} or \
                    not str(first) == str(second):
                diffs.append('Values differ: {first} != {second} at [{path}]'.format(
                    path=joined_path,
                    first=first,
                    second=second
                ))

        return diffs
