# Base test file to ensure functionality of the test environment
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4