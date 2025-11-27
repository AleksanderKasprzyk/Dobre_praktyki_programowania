from prime import is_prime


def test_is_prime_basic():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(5) is True
    assert is_prime(97) is True


def test_is_not_prime_basic():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(4) is False
    assert is_prime(9) is False
    assert is_prime(100) is False


def test_is_prime_negative_and_non_int():
    assert is_prime(-7) is False
    assert is_prime(-1) is False
    assert is_prime(3.5) is False