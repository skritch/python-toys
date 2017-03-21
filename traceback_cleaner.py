"""
V0.01

Some exception formatters

# global
sys.excepthook = print_clean_exc

# or as a formatter
class NiceExcFormatter(logging.Formatter):
    def formatException(self, ei):
        return format_clean_exc(*ei)

A few ideas:
- remove all lib/python code
- remove tornado concurrency code only
- accept a list of functions (partially applied filters/maps) to apply
- show offending value for relevant errors. (http://www.creativelydo.com/blog/how-to-globally-customize-exceptions-in-python/)
- other formatting options that make use of the func_code
"""


import sys
import traceback


def tb_cleaner(filename_filter):
    """
    Usage:

    Globally hide built-in modules from tracebacks (probably a bad idea):
    >>> remove_builtins = tb_cleaner(lambda fn:  fn.endswith('.py') and 'lib/python' not in fn)
    >>> def print_clean_exc(*ei):
    >>>     print(remove_builtins(*ei), file=sys.stderr)
    >>> sys.excepthook = print_clean_exc

    Hide concurrency crap from logs when using tornado:
    >>> import logging
    >>> remove_tornado = tb_cleaner(
    >>>     lambda fn: not (fn.endswith('tornado/gen.py') or fn.endswith('tornado/concurrent.py') )
    >>> )
    >>> class CleanExcFormatter(logging.Formatter):
    >>>     def formatException(self, ei):
    >>>          return remove_tornado(*ei)
    >>> sh = logging.StreamHandler(sys.stderr)
    >>> sh.setFormatter(CleanExcFormatter)
    """

    def format_tb_with_filter(etype, value, tb):
        tb_frames = traceback.extract_tb(tb)
        cleaned_tb = filter(
            # tb_frame[0] in python2
            lambda tb_frame: filename_filter(tb_frame.filename),
            tb_frames
        )
        exc_list = []
        if cleaned_tb:
            exc_list.append('Traceback (most recent call last):\n')
        exc_list = exc_list + traceback.format_list(cleaned_tb) + traceback.format_exception_only(etype, value)
        return ''.join(exc_list)

    return format_tb_with_filter

# inspired by http://www.creativelydo.com/blog/how-to-globally-customize-exceptions-in-python/
def debug_with_values():
    pass