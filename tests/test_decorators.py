import pytest

import iudex


def test_outer_decorator_is_seen(pre_and_post):
    @pre_and_post(lambda x: False)
    @pre_and_post(lambda x: True)
    def noop(x):
        return x

    with pytest.raises(iudex.exceptions.TestFailed):
        noop(None)


def test_inner_decorator_is_seen(pre_and_post):
    @pre_and_post(lambda x: True)
    @pre_and_post(lambda x: False)
    def noop(x):
        return x

    with pytest.raises(iudex.exceptions.TestFailed):
        noop(None)


def test_inner_invariant(pre_and_post):
    @pre_and_post(lambda x: True)
    @iudex.invariant(lambda x: len(x))
    def app(x):
        x.append(None)

    with pytest.raises(iudex.exceptions.InvariantViolated):
        app([])


def test_outer_invariant(pre_and_post):
    @iudex.invariant(lambda x: len(x))
    @pre_and_post(lambda x: True)
    def app(x):
        x.append(None)

    with pytest.raises(iudex.exceptions.InvariantViolated):
        app([])
