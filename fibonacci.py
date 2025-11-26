"""
fibonacci(n: int) → int - zwraca n-ty element ciągu Fibonacciego Załóż, że
fibonacci(0)  0 ,
fibonacci(1)  1 .)
"""

def fibonacci(n: int) -> int:
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b