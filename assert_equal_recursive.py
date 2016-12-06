import unittest
from itertools import izip_longest


class TestRecursive(unittest.TestCase):
    def assertEqualRecursive(self, first, second):
        """
        Asserts that two nested JSON-like structures consisting of dictionaries and lists are fully equal.
        """
        paths = self._check_equal_recursive(first, second)
        if paths:
            msg = '\n' + '\n'.join(paths)
            raise self.failureException(msg)

    def _check_equal_recursive(self, first, second, *path_so_far):
        diffs = []
        if isinstance(first, list) and isinstance(second, list):
            for i, (f, s) in enumerate(izip_longest(first, second)):
                diffs.extend(
                    self._check_equal_recursive(f, s, str(i), *path_so_far)
                )
        elif isinstance(first, dict) and isinstance(second, dict):
            for k in (first.viewkeys() | second.viewkeys()):
                diffs.extend(
                    self._check_equal_recursive(first.get(k), second.get(k), k, *path_so_far)
                )
        elif not first == second:
            joined_path = ']['.join(reversed(path_so_far))
            if type(first) == type(second):
                diffs.append('Values differ: {first} != {second} at [{path}]: '.format(
                    path=joined_path,
                    first=str(first),
                    second=str(second)
                ))
            else:
                diffs.append('Types differ: {first} != {second} at [{path}]: '.format(
                    path=joined_path,
                    first=type(first),
                    second=type(second)
                ))
        return diffs

