# services.py
from typing import Optional
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from config import DefaultConfig

# --- Azure Text Analytics client (lazy init) ---
_cfg = DefaultConfig()
_ta_client: Optional[TextAnalyticsClient] = None

def _client() -> TextAnalyticsClient:
    """Create/reuse a singleton TA client using keys from config.py/.env."""
    global _ta_client
    if _ta_client is None:
        _ta_client = TextAnalyticsClient(
            endpoint=_cfg.AZURE_LANGUAGE_ENDPOINT,
            credential=AzureKeyCredential(_cfg.AZURE_LANGUAGE_KEY),
        )
    return _ta_client

def get_sentiment(text: str) -> str:
    """Return overall sentiment label for a single text: 'positive'|'neutral'|'negative'|'mixed'.
    If anything fails, return 'unknown' (fail-safe for demos)."""
    if not text:
        return "unknown"
    try:
        result = _client().analyze_sentiment([text])[0]
        return result.sentiment or "unknown"
    except Exception:
        return "unknown"

# --- Rule-based replies (existing bot behavior) + sentiment branch ---
def get_response(intent: str, user_text: str = "") -> str:
    """Map an intent label to a canned response (traditional, non-LLM rules).
    Adds a 'sentiment' branch that uses Azure Text Analytics."""
    if intent == "greeting":
        return "Hello! How can I help you today?"
    elif intent == "help":
        return "Sure! You can ask me about FAQs, recommendations, or leave feedback."
    elif intent == "faq":
        return "Frequently asked questions will be supported here in the future."
    elif intent == "recommend":
        return "I can recommend resources once that feature is implemented."
    elif intent == "feedback":
        return "Thanks for your feedback! We will use it to improve."
    elif intent == "sentiment":
        s = get_sentiment(user_text)
        return f"Sentiment looks **{s}**."
    else:
        return "Sorry, I didn’t quite understand. Can you rephrase?"

    

    

