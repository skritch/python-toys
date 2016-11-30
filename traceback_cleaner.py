"""
V0.01

A few ideas:
- remove all lib/python code
- remove tornado concurrency code only
- accept a list of functions (partially applied filters/maps) to apply
- show offending value for relevant errors. (http://www.creativelydo.com/blog/how-to-globally-customize-exceptions-in-python/)
- other formatting options that make use of the func_code
"""


import sys
import traceback
from tornado import gen


def inner_func():
    raise Exception('Inner exception')


@gen.coroutine
def inner_co():
    raise gen.Return(inner_func())


@gen.coroutine
def outer_co():
    yield inner_co()


def format_clean_exc(etype, value, tb):
    tb_frames = traceback.extract_tb(tb)
    cleaned_tb = filter(
        lambda tb_frame: 'lib/python' not in tb_frame.filename and tb_frame.filename[-3:] == '.py',
        tb_frames
    )
    exc_list = []
    if cleaned_tb:
        exc_list.append('Traceback (most recent call last):\n')
    exc_list = exc_list + traceback.format_list(cleaned_tb) + traceback.format_exception_only(etype, value)
    return ''.join(exc_list)


def print_clean_exc(etype, value, tb):
    print(format_clean_exc(etype, value, tb), file=sys.stderr)


# global
sys.excepthook = print_clean_exc


if __name__ == '__main__':
    try:
        fut = outer_co()
        result = fut.result()
    except Exception:
        #print_clean_exc(*sys.exc_info())
        raise


