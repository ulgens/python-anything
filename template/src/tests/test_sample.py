# https://docs.pytest.org/en/stable/#a-quick-example
def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4
