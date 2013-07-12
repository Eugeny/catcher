from collections import namedtuple
import sys
import time
import inspect

Report = namedtuple('Report', ['timestamp', 'exception', 'traceback'])
Frame = namedtuple('Frame', ['file', 'line', 'code', 'locals'])


def __collect_frame(frame):
    return Frame(
        file=inspect.getfile(frame),
        line=frame.f_lineno,
        locals=frame.f_locals,
        code=inspect.getsourcelines(frame),
    )


def collect(exception):
    exc_info = sys.exc_info()
    traceback = []

    tb = exc_info[2]
    while tb:
        frame = tb.tb_frame
        traceback.append(__collect_frame(frame))
        tb = tb.tb_next

    return Report(
        timestamp=time.time(),
        exception=exception,
        traceback=traceback,
    )
