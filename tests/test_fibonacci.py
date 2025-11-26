from fibonacci import fibonacci


def test_fibonacci_values():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55


def test_fibonacci_negative_raises():
    from pytest import raises

    with raises(ValueError):
        fibonacci(-1)