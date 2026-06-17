"""
PII Redaction module.

Detects and masks personally identifiable / sensitive information
(credit card numbers, emails, phone numbers) in customer messages
BEFORE that text is ever sent to the LLM. This mirrors the tutorial's
first pipeline step: never let sensitive data leave your system to a
third-party model unmasked.
"""

import re
from typing import Tuple, List

# Patterns are intentionally conservative (favor catching too much over
# leaking real data). Order matters: check credit cards before generic
# digit sequences like phone numbers.

CREDIT_CARD_PATTERN = re.compile(
    r"\b(?:\d[ -]*?){13,16}\b"
)
EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)
PHONE_PATTERN = re.compile(
    r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
)


def redact_pii(text: str) -> Tuple[str, List[str]]:
    """
    Returns (redacted_text, list_of_pii_types_found).

    Order of operations matters: credit cards are masked first since a
    16-digit card number would otherwise also match looser phone patterns.
    """
    found = []
    redacted = text

    if CREDIT_CARD_PATTERN.search(redacted):
        found.append("credit_card")
        redacted = CREDIT_CARD_PATTERN.sub("[REDACTED_CARD]", redacted)

    if EMAIL_PATTERN.search(redacted):
        found.append("email")
        redacted = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", redacted)

    if PHONE_PATTERN.search(redacted):
        found.append("phone")
        redacted = PHONE_PATTERN.sub("[REDACTED_PHONE]", redacted)

    return redacted, found


if __name__ == "__main__":
    sample = (
        "I'm absolutely furious my package was supposed to arrive 5 days ago "
        "and still hasn't shown up. My email is jane.doe@example.com and my "
        "card number is 4111 1111 1111 1111. Call me at 555-123-4567."
    )
    clean, types = redact_pii(sample)
    print("Original: ", sample)
    print("Redacted: ", clean)
    print("PII found:", types)
