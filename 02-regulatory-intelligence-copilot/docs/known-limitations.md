# Known Limitations & Compliance Disclaimers

## 1. 100% Synthetic Data Boundary
- All regulatory guidance comparisons, submission impact mappings, and protocol references are synthetic and provided for demonstration and algorithmic evaluation only.
- Official regulatory submissions must rely on verified agency publications directly from FDA.gov, EMA.europa.eu, or ICH.org.

---

## 2. Decision Support Only
- The copilot provides informational and drafting support.
- In accordance with global regulatory practices, final submission dossier filings and interpretations require sign-off by a qualified Regulatory Affairs Professional (`REGULATORY_REVIEWER`).
- Autonomous regulatory filing without human review is strictly prohibited.

---

## 3. Local Execution Assumptions
- Local development utilizes SQLite (`regulatory_intelligence.db`) for zero-dependency portability. Docker Compose provides PostgreSQL 16 + pgvector for full production environments.
- Fallback mechanisms guarantee offline test execution without external API keys.
