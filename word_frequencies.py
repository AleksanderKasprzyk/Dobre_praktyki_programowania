# word_frequencies.py
import re
from collections import Counter

def word_frequencies(text: str) -> dict:
    if not text:
        return {}

    # usuwamy interpunkcję, zostawiamy litery, cyfry i spacje
    cleaned = re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
    words = [w.lower() for w in cleaned.split() if w.strip()]

    return dict(Counter(words))
