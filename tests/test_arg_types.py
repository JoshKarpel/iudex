import pytest

import iudex


def test_single_positional_arg():
    @iudex.pre(lambda x: x == 0)
    def noop(x):
        return x

    with pytest.raises(iudex.exceptions.TestFailed):
        noop(None)


def test_multiple_positional_args():
    @iudex.pre(lambda x, y: x == y)
    def noop(x, y):
        return x, y

    with pytest.raises(iudex.exceptions.TestFailed):
        noop(0, 1)


def test_keyword_args_passed_as_keyword():
    @iudex.pre(lambda p: p == None)
    def noop(p = None):
        return p

    with pytest.raises(iudex.exceptions.TestFailed):
        noop(p = 0)


def test_keyword_args_passed_as_positional():
    @iudex.pre(lambda p: p == None)
    def noop(p = None):
        return p

    with pytest.raises(iudex.exceptions.TestFailed):
        noop(0)


def test_keyword_args_in_lambda_passed_as_positional():
    @iudex.pre(lambda p = 5: p == None)
    def noop(p = None):
        return p

    with pytest.raises(iudex.exceptions.TestFailed):
        noop(0)
