"""
count_vowels(text: str) → int - zlicza liczbę samogłosek w podanym ciągu (a, e, i, o, u,
y – wielkość liter bez znaczenia).
"""

def count_vowels(text: str) -> int:
    if not text:
        return 0

    vowels = set("aeiouyąęó")

    return sum(1 for ch in text.lower() if ch in vowels)
