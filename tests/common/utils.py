import signal
from contextlib import contextmanager

from tests.common.exception import SignalTimeoutException


@contextmanager
def time_limit(seconds):
    '''
    Context manager (with statement) to handle long function calls.
    Needed to test the while loop in Listener

    :param seconds: time before stop
    '''
    def signal_handler(signum, frame):
        raise SignalTimeoutException('{sec} seconds are over!'.format(sec=seconds))

    # Sets a timeout using signal
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        signal.alarm(0)
