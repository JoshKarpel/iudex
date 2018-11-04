import pytest

import iudex


@pytest.fixture(params = [iudex.pre, iudex.post])
def pre_and_post(request):
    return request.param
