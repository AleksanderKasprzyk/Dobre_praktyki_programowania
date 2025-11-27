from word_frequencies import word_frequencies


def test_word_frequencies_simple():
    result = word_frequencies("To be or not to be")
    assert result == {"to": 2, "be": 2, "or": 1, "not": 1}


def test_word_frequencies_punctuation():
    result = word_frequencies("Hello, hello!")
    assert result == {"hello": 2}


def test_word_frequencies_empty():
    assert word_frequencies("") == {}


def test_word_frequencies_mixed_case():
    result = word_frequencies("Python PYTHON python")
    assert result == {"python": 3}

def test_word_frequencies_polish():
    result = word_frequencies("Ala ma kota, a kot ma Ale.")
    # ważne: wszystkie na małe litery
    assert result == {
        "ala": 1,
        "ma": 2,
        "kota": 1,
        "a": 1,
        "kot": 1,
        "ale": 1,
    }
