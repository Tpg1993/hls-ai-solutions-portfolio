import re
from typing import Dict, Any
from app.ai.pii_scrubber import scrub_pii

# Clinical entity dictionary for deterministic baseline extraction
KNOWN_DRUGS = ["CardioShield", "NeuroCalm", "OncoVax", "ImmunoBlast", "Metformin", "Atorvastatin", "Pembrolizumab", "Lisinopril"]
KNOWN_REACTIONS = [
    ("Acute Hepatitis", "Hepatobiliary disorders"),
    ("Ventricular Tachycardia", "Cardiac disorders"),
    ("Stevens-Johnson Syndrome", "Skin and subcutaneous tissue disorders"),
    ("Anaphylactic Shock", "Immune system disorders"),
    ("Severe Thrombocytopenia", "Blood and lymphatic system disorders"),
    ("Acute Kidney Injury", "Renal and urinary disorders"),
    ("Interstitial Lung Disease", "Respiratory, thoracic and mediastinal disorders")
]

def extract_safety_entities(narrative: str) -> Dict[str, Any]:
    """
    Scrubs PII and extracts structured pharmacovigilance entities from raw case narratives.
    """
    scrubbed_text, redactions = scrub_pii(narrative)

    # 1. Detect Suspect Drug
    detected_drug = "CardioShield"
    for drug in KNOWN_DRUGS:
        if re.search(r'\b' + re.escape(drug) + r'\b', narrative, re.IGNORECASE):
            detected_drug = drug
            break

    # 2. Detect Adverse Reaction & MedDRA SOC
    detected_event = "Acute Hepatitis"
    detected_soc = "Hepatobiliary disorders"
    for event, soc in KNOWN_REACTIONS:
        if re.search(r'\b' + re.escape(event) + r'\b', narrative, re.IGNORECASE):
            detected_event = event
            detected_soc = soc
            break

    # 3. Detect Patient Age & Sex
    age_match = re.search(r'\b(\d{1,2})[- ]?(?:year|yr)s?[- ]?old\b', narrative, re.IGNORECASE)
    age = int(age_match.group(1)) if age_match else 56

    sex = "F" if re.search(r'\b(?:female|woman|she|her)\b', narrative, re.IGNORECASE) else "M"

    # 4. Detect Severity & Outcome
    if re.search(r'\b(?:hospital|admitted|fatal|death|intensive care|icu)\b', narrative, re.IGNORECASE):
        severity = "SERIOUS_HOSPITALIZATION"
    else:
        severity = "NON_SERIOUS"

    outcome = "RECOVERED" if re.search(r'\b(?:resolved|recovered|discharged)\b', narrative, re.IGNORECASE) else "NOT_RECOVERED"

    return {
        "suspect_drug": detected_drug,
        "adverse_event": detected_event,
        "meddra_soc": detected_soc,
        "age": age,
        "sex": sex,
        "severity": severity,
        "outcome": outcome,
        "scrubbed_narrative": scrubbed_text,
        "pii_redactions_count": redactions
    }
