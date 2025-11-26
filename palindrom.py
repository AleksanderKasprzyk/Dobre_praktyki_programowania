"""
1. is_palindrome(text: str) -> bool - sprawdza, czy dany ciąg znaków jest palindromem
(ignorując wielkość liter i spacje).
"""
import re

def is_palindrome(text: str) -> bool:
    if text is None:
        return False
    cleaned_text = re.sub(r'[\W_]+', '', text).lower()
    return cleaned_text == cleaned_text[::-1]
