import pytest
from app.ai.extractor import extract_safety_entities
from app.ai.pii_scrubber import scrub_pii

def test_pii_scrubbing_redaction():
    raw_text = "Patient John Doe (email: john.doe@example.com, phone: 555-123-4567) was seen by Dr. Smith with MRN 12345678."
    scrubbed, count = scrub_pii(raw_text)
    
    assert "[REDACTED_EMAIL]" in scrubbed
    assert "[REDACTED_PHONE]" in scrubbed
    assert "[REDACTED_IDENTIFIER]" in scrubbed
    assert count >= 3
    assert "john.doe@example.com" not in scrubbed
    assert "555-123-4567" not in scrubbed

def test_entity_extraction_safety_narrative():
    narrative = (
        "A 64-year-old female was administered CardioShield 50mg daily. Two weeks later, "
        "she presented to the emergency room with jaundice and was admitted to the hospital "
        "with diagnosed Acute Hepatitis. Transaminases were markedly elevated."
    )
    result = extract_safety_entities(narrative)
    
    assert result["suspect_drug"] == "CardioShield"
    assert result["adverse_event"] == "Acute Hepatitis"
    assert result["meddra_soc"] == "Hepatobiliary disorders"
    assert result["age"] == 64
    assert result["sex"] == "F"
    assert result["severity"] == "SERIOUS_HOSPITALIZATION"
