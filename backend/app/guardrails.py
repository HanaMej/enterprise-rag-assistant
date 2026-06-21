SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "ignore the context",
    "reveal your system prompt",
    "show your system prompt",
    "forget all instructions",
    "act as",
    "jailbreak",
    "developer message",
    "system message",
]


def is_safe_question(question: str) -> bool:
    question_lower = question.lower()

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in question_lower:
            return False

    return True