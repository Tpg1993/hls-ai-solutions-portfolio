# Security & Compliance Architecture: Pharmacovigilance Platform

## 1. Role-Based Access Control (RBAC)

Authorization is strictly enforced on the FastAPI backend via route dependencies (`app.core.security.require_role`). Default policy is **Deny by Default**.

| Role | Level | Permissions | Scope |
| :--- | :---: | :--- | :--- |
| **SUPER_ADMIN** | 100 | System & tenant settings, user provisioning, telemetry | Full administrative control |
| **ADMIN** | 80 | User management, dictionary management, cache flushing | Operational administration |
| **SAFETY_REVIEWER**| 60 | Sign off safety signals, record disposition decisions, add medical notes | Mandatory physician approval gate |
| **ANALYST** | 40 | Ingest case narratives, trigger entity extraction, query safe NL2SQL | Case processing and triage |
| **AUDITOR** | 20 | Read-only inspection of immutable regulatory audit trails | Compliance inspection |
| **STANDARD_USER** | 10 | Read-only view of public dashboards | General oversight |

---

## 2. Threat Modeling & Safeguards

### A. Patient Privacy & PHI Anonymization
- All adverse event narratives undergo automated PII redaction prior to database storage or LLM processing.
- Synthetic datasets exclusively: No real patient identifiers or commercial batch numbers are processed.
- Prominent UI disclaimer: `"SYNTHETIC / DEMO DATA ONLY — DECISION SUPPORT ENVIRONMENT"`.

### B. Safe Read-Only NL2SQL
- AST validation via `sqlparse`: Only `SELECT` statements permitted.
- Keyword blacklist: Any DDL/DML attempt (`DROP`, `DELETE`, `INSERT`, `UPDATE`, `ALTER`, `TRUNCATE`, `EXEC`) is rejected with `400 Bad Request`.
- Schema allowlisting: Queries restricted to `safety_cases`, `safety_signals`, `safety_reviews`, and `evidence_documents`.

### C. Zero Secret Leakage
- LLM API keys (`SARVAM_API_KEY`, `OPENAI_API_KEY`) and JWT secrets reside exclusively in server-side `.env`.
- No sensitive keys are exposed to the browser.
