import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from palindrom import is_palindrome

# ---------- test ----------
def test_is_palindrome():
    assert is_palindrome("kajak") is True
    assert is_palindrome("Kobyła ma mały bok") is True
    assert is_palindrome("python") is False
    assert is_palindrome("") is True
    assert is_palindrome("A") is True
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("No 'x' in Nixon") is True
    assert is_palindrome("12321") is True
    assert is_palindrome("12345") is False
