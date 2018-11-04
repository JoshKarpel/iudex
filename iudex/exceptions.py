class IudexException(Exception):
    pass


class TestFailed(IudexException):
    pass


class InvariantViolated(IudexException):
    pass
