from vowels import count_vowels


def test_count_vowels_basic():
    assert count_vowels("Python") == 2
    assert count_vowels("AEIOUY") == 6
    assert count_vowels("bcd") == 0
    assert count_vowels("") == 0


def test_count_vowels_polish_characters():
    assert count_vowels("Próba żółwia") == 5
