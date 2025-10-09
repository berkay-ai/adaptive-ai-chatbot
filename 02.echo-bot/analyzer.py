from langdetect import detect, DetectorFactory
from nltk.sentiment import SentimentIntensityAnalyzer

# Make language detection deterministic
DetectorFactory.seed = 0

# Global VADER analyzer (cheap to reuse)
_sia = SentimentIntensityAnalyzer()

# Heuristics for Turkish detection
TR_CHARS = set("çğıöşüÇĞİÖŞÜ")
TR_COMMON = {
    "merhaba","selam","teşekkür","teşekkürler","rica","evet","hayır","değil",
    "nasılsın","lütfen","yardım","çalışmıyor","hata","sorun","için","neden","nerede","şimdi"
}


def _looks_turkish(text: str) -> bool:
    """Heuristic: Turkish-specific letters or very common Turkish words."""
    t = (text or "").strip()
    if not t:
        return False
    low = t.lower()
    if any(ch in TR_CHARS for ch in low):
        return True
    words = {w.strip(".,!?;:()[]\"'") for w in low.split()}
    if words & TR_COMMON:
        return True
    return False


def detect_language(text: str) -> str:
    """
    Detects text language and returns 'tr' or 'en'.
    Heuristic gets priority for short inputs; falls back to langdetect.
    """
    t = (text or "").strip()
    if not t:
        return "en"

    # Heuristic first for very short inputs (1–2 words or < 6 chars)
    short_input = len(t) < 6 or len(t.split()) <= 2
    if short_input and _looks_turkish(t):
        return "tr"

    # General heuristic (helps even for longer messages)
    if _looks_turkish(t):
        return "tr"

    # Fallback to langdetect
    try:
        code = detect(t)
    except Exception:
        return "en"
    return "tr" if code.startswith("tr") else "en"


def analyze_sentiment(text: str, lang: str = "en") -> str:
    """
    Returns sentiment label: 'pos', 'neu', or 'neg'.
    Uses VADER compound score; reinforces with tiny Turkish lexicon heuristics.
    """
    t = (text or "").strip()
    if not t:
        return "neu"

    score = _sia.polarity_scores(t)["compound"]
    label = "pos" if score >= 0.05 else "neg" if score <= -0.05 else "neu"

    if lang == "tr":
        low = t.lower()
        tr_neg = {"olmuyor","berbat","kötü","sinirliyim","üzgünüm","hata","problem","çalışmıyor","sıkıntı","kızgınım"}
        tr_pos = {"harika","mükemmel","süper","teşekkürler","şahane","müthiş","çözüldü","tamamdır","teşekkür","harika oldu"}
        if any(w in low for w in tr_neg):
            label = "neg"
        elif any(w in low for w in tr_pos):
            label = "pos"

    return label
