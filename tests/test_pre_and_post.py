import pytest

import iudex


def test_pre_raises_if_fail(pre_and_post):
    @pre_and_post(lambda x: x > 0)
    def noop(x):
        return x

    with pytest.raises(iudex.exceptions.TestFailed)as excinfo:
        noop(-1)


def test_source_in_msg_with_lambda(pre_and_post):
    @pre_and_post(lambda x: x > 0)
    def noop(x):
        return x

    with pytest.raises(iudex.exceptions.TestFailed) as excinfo:
        noop(-1)

    msg = str(excinfo.value)
    assert 'lambda x: x > 0' in msg


def test_source_in_msg_with_def(pre_and_post):
    def test(x):
        return x > 0

    @pre_and_post(test)
    def noop(x):
        return x

    with pytest.raises(iudex.exceptions.TestFailed) as excinfo:
        noop(-1)

    msg = str(excinfo.value)
    assert 'def test(x):' in msg
    assert 'return x > 0' in msg


def test_params_in_msg(pre_and_post):
    @pre_and_post(lambda x: x > 0)
    def noop(x):
        return x

    with pytest.raises(iudex.exceptions.TestFailed) as excinfo:
        noop(-1)

    msg = str(excinfo.value)
    assert 'x = -1' in msg


def test_post_can_see_return_value():
    @iudex.post(lambda rv: rv == 5)
    def zero():
        return 0

    with pytest.raises(iudex.exceptions.TestFailed):
        zero()


def test_return_value_is_returned_on_success(pre_and_post):
    @pre_and_post(lambda x: True)
    def noop(x):
        return x

    assert noop(1) == 1
