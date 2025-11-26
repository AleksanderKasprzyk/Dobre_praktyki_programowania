"""
calculate_discount(price: float, discount: float) → float - zwraca cenę po uwzględnieniu zniżki
(np. calculate_discount(100, 0.2  80). Jeśli discount jest spoza zakresu 01, ma zostać zgłoszony wyjątek
ValueError
"""

def calculate_discount(price: float, discount: float) -> float:
    if not (0 <= discount <= 1):
        raise ValueError("discount must be between 0 and 1")

    return price * (1 - discount)
