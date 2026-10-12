# Known Limitations & Compliance Boundaries

## 1. 100% Synthetic Data Boundary
- All case identifiers (`ICSR-2026-1004`), patient ages, narratives, and drug-event associations are completely synthetic.
- No real proprietary pharmacovigilance reports or patient Protected Health Information (PHI) are included.
- For demonstration and algorithmic evaluation only.

---

## 2. Decision Support Only — No Autonomous Medical Judgment
- The platform is an assistive AI copilot for evidence triage.
- In accordance with FDA 21 CFR Part 314.80, ICH E2B(R3), and GVP Module IX guidelines, final determination of drug-event causality, expectedness, and regulatory safety escalation remains the exclusive responsibility of qualified Safety Reviewers (`SAFETY_REVIEWER`).
- Autonomous safety dispositions are strictly prohibited.

---

## 3. Local Execution Assumptions
- Default local engine uses SQLite (`pharmacovigilance.db`) for immediate zero-dependency portability. Docker Compose provides PostgreSQL 16 + pgvector for full enterprise deployment.
- Offline fallback ensures full test suite execution without external paid API keys.
