

def is_prime(n: int) -> bool:

    if not isinstance(n, int):
        return False

    if n < 2:
        return False

    if n in (2, 3):
        return True

    if n % 2 == 0:
        return False

    limit = int(n ** 0.5) + 1
    for i in range(3, limit, 2):
        if n % i == 0:
            return False

    return True
