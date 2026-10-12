import re
from typing import Dict, Any, Tuple

# Regex patterns for fast deterministic PII/PHI scrubbing
PHONE_REGEX = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
SSN_MRN_REGEX = re.compile(r'\b(?:\d{3}-\d{2}-\d{4}|MRN:?\s*\d{6,10})\b', re.IGNORECASE)
NAME_TITLES_REGEX = re.compile(r'\b(?:Mr\.|Mrs\.|Ms\.|Dr\.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b')

def scrub_pii(text: str) -> Tuple[str, int]:
    """
    Redacts patient personal identifiable information (PII/PHI) from raw spontaneous reports.
    Returns (scrubbed_text, count_of_redactions).
    """
    if not text:
        return "", 0

    count = 0
    scrubbed = text

    # Redact Emails
    matches = EMAIL_REGEX.findall(scrubbed)
    count += len(matches)
    scrubbed = EMAIL_REGEX.sub("[REDACTED_EMAIL]", scrubbed)

    # Redact Phones
    matches = PHONE_REGEX.findall(scrubbed)
    count += len(matches)
    scrubbed = PHONE_REGEX.sub("[REDACTED_PHONE]", scrubbed)

    # Redact SSN / MRN
    matches = SSN_MRN_REGEX.findall(scrubbed)
    count += len(matches)
    scrubbed = SSN_MRN_REGEX.sub("[REDACTED_IDENTIFIER]", scrubbed)

    # Redact Names with Titles
    matches = NAME_TITLES_REGEX.findall(scrubbed)
    count += len(matches)
    scrubbed = NAME_TITLES_REGEX.sub("[REDACTED_NAME]", scrubbed)

    return scrubbed, count
