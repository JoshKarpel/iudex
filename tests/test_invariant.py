import pytest

import iudex


def test_invariant():
    @iudex.invariant(lambda x: len(x))
    def app(x):
        x.append(None)

    with pytest.raises(iudex.exceptions.InvariantViolated) as excinfo:
        app([])


def test_invariant_violated_msg_has_old_and_new_in_it():
    @iudex.invariant(lambda x: len(x))
    def app(x):
        x.append(None)

    with pytest.raises(iudex.exceptions.InvariantViolated) as excinfo:
        app([])

    msg = str(excinfo.value)
    assert '0' in msg
    assert '1' in msg
