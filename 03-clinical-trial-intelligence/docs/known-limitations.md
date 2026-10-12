# Known Limitations & Synthetic Data Disclaimers

## 1. 100% Synthetic Data Boundary
- All patient demographics, clinical notes, lab values, genomic biomarkers, and trial operational metrics are entirely synthetic.
- Synthetic patient identifiers (`PT-4091`) and clinical trial protocol numbers are generated for demonstration and evaluation purposes only.
- Under no circumstances should real patient Protected Health Information (PHI) or proprietary trial protocols be submitted without full de-identification and institutional review board (IRB) compliance.

---

## 2. Decision Support Only
- The matching engine and AI reasoning models provide **Decision Support Only**.
- In accordance with FDA 21 CFR Part 11 and Good Clinical Practice (GCP) guidelines, final patient eligibility determination requires formal sign-off by a qualified Principal Investigator (PI) or Clinical Reviewer (`CLINICAL_REVIEWER`).
- Autonomous enrollment without human validation is explicitly forbidden.

---

## 3. Local Demo Assumptions
- **Storage**: Default local setup uses SQLite (`clinical_trials.db`) for immediate zero-dependency portability. Docker Compose provides PostgreSQL 16 + pgvector for full enterprise deployment.
- **LLM Connectivity**: Sarvam AI (`sarvam-105b`) is used as primary provider; in environments without API keys configured, deterministic fallback rule sets guarantee full offline functionality.
