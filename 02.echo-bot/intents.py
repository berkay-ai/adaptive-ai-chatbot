def get_intent(message: str) -> str:
    """Rule-based intent classifier.
    Returns one of: 'greeting', 'help', 'faq', 'recommend', 'feedback', or 'fallback'.
    """
    message = message.lower()

    # greeting keywords
    if "hello" in message or "hi" in message:
        return "greeting"
    # help command
    elif "help" in message:
        return "help"
    # simple faq trigger
    elif "faq" in message or "question" in message:
        return "faq"    # sentiment analysis request
    elif "sentiment" in message or "mood" in message or "feeling" in message:
        return "sentiment"
    # future assignments: recommendation stub
    elif "recommend" in message:
        return "recommend"
    # collect user feedback
    elif "feedback" in message:
        return "feedback"
    # default path
    else:
        return "fallback"  # fallback for unknown messages

