from six import PY2

if PY2:
    class TimeoutError(Exception):
        pass


class SignalTimeoutException(TimeoutError):
    pass
