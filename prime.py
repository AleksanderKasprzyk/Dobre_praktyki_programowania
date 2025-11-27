# is_prime.py

def is_prime(n: int) -> bool:
    # liczby mniejsze niż 2 nie są pierwsze
    if not isinstance(n, int):
        return False

    if n < 2:
        return False

    # 2 i 3 są pierwsze
    if n in (2, 3):
        return True

    # liczby parzyste > 2 nie są pierwsze
    if n % 2 == 0:
        return False

    # sprawdzamy dzielniki od 3 do sqrt(n), tylko nieparzyste
    limit = int(n ** 0.5) + 1
    for i in range(3, limit, 2):
        if n % i == 0:
            return False

    return True
