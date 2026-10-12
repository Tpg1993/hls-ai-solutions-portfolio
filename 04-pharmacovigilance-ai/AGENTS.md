# AGENTS.md — Project 04: AI Pharmacovigilance & Safety Signal Intelligence Platform

> Adheres strictly to the mandatory root guidelines defined in [../AGENTS.md](../AGENTS.md).

## Non-Negotiable Core Rules
1. **Local-First Full Stack**: FastAPI Python 3.12 backend + Next.js React TypeScript frontend + SQLite/PostgreSQL with pgvector.
2. **Zero Hardcoded Secrets & Absolute Paths**: Only relative paths and `.env.example` placeholders.
3. **Deterministic Disproportionality Metrics**: PRR, ROR, 95% confidence intervals, and Chi-square calculations MUST be deterministic Python code with zero LLM estimation or fabrication.
4. **Mandatory Human Safety Sign-Off**: The AI prepares entity extractions, disproportionality metrics, and evidence summaries; it NEVER autonomously determines drug causality or legal/regulatory disposition. `SAFETY_REVIEWER` sign-off is mandatory.
5. **Presidio PII/PHI Scrubbing**: Spontaneous narrative text must be scrubbed of patient identifiers prior to storage or LLM processing.
6. **Synthetic Safety Data Only**: All ICSR cases and drug-event records are 100% synthetic. Clear visual disclaimers must be displayed across all UI and API responses.
