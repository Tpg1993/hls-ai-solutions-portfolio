from typing import Tuple
from app.core.logging import logger

_analyzer = None
_anonymizer = None
_init_attempted = False

def _get_presidio_engines():
    global _analyzer, _anonymizer, _init_attempted
    if not _init_attempted:
        _init_attempted = True
        try:
            from presidio_analyzer import AnalyzerEngine
            from presidio_anonymizer import AnonymizerEngine
            _analyzer = AnalyzerEngine()
            _anonymizer = AnonymizerEngine()
        except Exception as e:
            logger.info(f"Presidio model not pre-downloaded, using fast regex PII scrubbing: {e}")
            _analyzer = None
            _anonymizer = None
    return _analyzer, _anonymizer

class PresidioSanitizer:
    """
    Sanitizes PII/PHI (names, phone numbers, emails, addresses)
    before sending prompts to external LLMs.
    """
    def sanitize(self, text: str) -> Tuple[str, bool]:
        if not text or not text.strip():
            return text, False

        if _PRESIDIO_AVAILABLE:
            try:
                results = _analyzer.analyze(text=text, language="en")
                if results:
                    anonymized_result = _anonymizer.anonymize(text=text, analyzer_results=results)
                    return anonymized_result.text, True
            except Exception as exc:
                logger.warning(f"Presidio analysis encountered an error: {exc}")

        # Basic regex scrubbing fallback for emails and phone numbers
        import re
        sanitized = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '<EMAIL_REDACTED>', text)
        sanitized = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '<PHONE_REDACTED>', sanitized)
        modified = sanitized != text
        return sanitized, modified

presidio_sanitizer = PresidioSanitizer()
