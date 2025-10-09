from typing import List, Dict
import logging

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount

from intents import get_intent
from services import get_response
from analyzer import detect_language, analyze_sentiment

logger = logging.getLogger(__name__)

# ------------------ In-memory session preferences ------------------
# For assignment/demo only. In production, persist via ConversationState/UserState.
PREFS: Dict[str, Dict[str, str]] = {}  # { conversation_id: {"length": "short|long", "tone": "formal|casual"} }


def _conv_id(ctx: TurnContext) -> str:
    """Returns a stable conversation id key for storing preferences."""
    conv = ctx.activity.conversation
    return conv.id or "default"


def _style_by_prefs(text: str, prefs: Dict[str, str], lang: str) -> str:
    """Adjust reply length and tone according to stored preferences."""
    length = prefs.get("length", "long")   # default: long
    tone   = prefs.get("tone", "formal")   # default: formal

    # Length control
    if length == "short":
        first_line = text.split("\n")[0]         # keep first line/sentence
        cut = first_line[:100].rstrip()
        if len(first_line) > 100:
            cut += "…"
        text = cut

    # Tone control (very light rewrite for "casual")
    if tone == "casual":
        if lang == "tr":
            text = text.replace("Yardımcı olmak için buradayım.", "Buradayım, hallederiz.")
            text = text.replace("Lütfen", "Lütfen :)")
        else:
            text = text.replace("Happy to help.", "I’m here for you :)")
            text = text.replace("Let’s go step by step:", "Let’s do it step by step:")

    return text
# -------------------------------------------------------------------


class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self,
        members_added: List[ChannelAccount],
        turn_context: TurnContext,
    ):
        """Send a welcome message when a new member joins the conversation."""
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(MessageFactory.text("Hello and welcome!"))

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Classify intent, detect language, analyze sentiment, apply preferences,
        call service, and send the reply.
        """
        user_text = (turn_context.activity.text or "").strip()

        # ---------- 0) Slash commands (handled immediately) ----------
        conv_id = _conv_id(turn_context)
        prefs   = PREFS.setdefault(conv_id, {})  # ensure bucket exists

        if user_text.startswith("/"):
            cmd = user_text.lower().split()[0]
            if cmd == "/short":
                prefs["length"] = "short"
                await turn_context.send_activity(MessageFactory.text("Preference set: short replies."))
                return
            if cmd == "/long":
                prefs["length"] = "long"
                await turn_context.send_activity(MessageFactory.text("Preference set: long replies."))
                return
            if cmd == "/formal":
                prefs["tone"] = "formal"
                await turn_context.send_activity(MessageFactory.text("Preference set: formal tone."))
                return
            if cmd == "/casual":
                prefs["tone"] = "casual"
                await turn_context.send_activity(MessageFactory.text("Preference set: casual tone."))
                return
            if cmd == "/reset":
                prefs.clear()
                await turn_context.send_activity(MessageFactory.text("Preferences reset to defaults."))
                return
            await turn_context.send_activity(MessageFactory.text(
                "Unknown command. Try /short, /long, /formal, /casual, or /reset."
            ))
            return
        # -------------------------------------------------------------

        # 1) Language detection
        lang = detect_language(user_text)

        # 2) Sentiment analysis
        sentiment = analyze_sentiment(user_text, lang=lang)

        # 3) Existing intent/response
        intent = get_intent(user_text)
        reply  = get_response(intent, user_text)

        # 3.1) Normalize generic fallbacks (both EN and TR paths will use our defaults)
        EN_GENERIC = {
            "Hello! How can I help you today?",
            "Sorry, I didn’t quite understand. Can you rephrase?",
            "Sorry, I didn't quite understand. Can you rephrase?",
        }
        if not reply or reply.strip() in EN_GENERIC:
            reply = None  # prefer our language+sentiment default below

        # 4) Language+sentiment default templates and tags
        if lang == "tr":
            if sentiment == "neg":
                default_reply = (
                    "Anlıyorum, bu can sıkıcı olabilir. Küçük adımlarla ilerleyelim:\n"
                    "1) Hata tam olarak nerede görünüyor?\n"
                    "2) Kullandığın komutu/ekranı paylaş, birlikte deneyelim."
                )
                tag = "[TR][NEG]"
            elif sentiment == "pos":
                default_reply = "Harika! Bir sonraki adımı deneyelim. Nereden devam edelim?"
                tag = "[TR][POS]"
            else:
                default_reply = "Yardımcı olmak için buradayım. Tam olarak ne yapmak istiyorsun?"
                tag = "[TR][NEU]"
        else:
            if sentiment == "neg":
                default_reply = (
                    "I get this can be frustrating. Let’s go step by step:\n"
                    "1) Where exactly do you see the error?\n"
                    "2) Share the command/screen and we’ll try together."
                )
                tag = "[EN][NEG]"
            elif sentiment == "pos":
                default_reply = "Awesome! Want to try the next step? Where should we go next?"
                tag = "[EN][POS]"
            else:
                default_reply = "Happy to help. What would you like to do exactly?"
                tag = "[EN][NEU]"

        # 5) Prefer existing reply; fallback to our default
        base_reply = reply or default_reply

        # 5.1) Apply user preferences (length/tone)
        styled = _style_by_prefs(base_reply, prefs, lang)

        # 5.2) Compose final message
        reply_text = f"{tag} {styled}"

        # 6) Log with preferences snapshot
        logger.info(
            "Intent=%s | Lang=%s | Sentiment=%s | Prefs=%s | Text=%s | Reply=%s",
            intent, lang, sentiment, prefs, user_text, reply_text,
        )

        # 7) Send
        await turn_context.send_activity(MessageFactory.text(reply_text))
