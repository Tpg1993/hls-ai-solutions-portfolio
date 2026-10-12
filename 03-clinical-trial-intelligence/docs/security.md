# Security & Governance Architecture: Clinical Trial Intelligence

## 1. Role-Based Access Control (RBAC) Matrix

Authorization is strictly enforced in the FastAPI backend via dependency injection (`app.core.security.require_role`). Default policy is **Deny by Default**.

| Role | Level | Permissions | Clinical Scope |
| :--- | :---: | :--- | :--- |
| **SUPER_ADMIN** | 100 | System settings, user provisioning, global telemetry | Full system administration |
| **ADMIN** | 80 | User management, site configuration, model retraining | Administrative operations |
| **CLINICAL_REVIEWER** | 60 | Review patient matches, approve/reject/modify match status, sign off audits | Clinical decision sign-off |
| **ANALYST** | 40 | Search trials, run eligibility checks, query ClinOps NL2SQL, view forecasts | Read-write exploratory research |
| **AUDITOR** | 20 | Read-only access to immutable clinical decision audit trails | Regulatory compliance inspection |
| **STANDARD_USER** | 10 | Read-only view of public trial catalog | Basic trial browsing |

---

## 2. Threat Modeling & Defense Strategies

### A. Synthetic Data & Zero PHI Leakage
- **100% Synthetic Data**: All patient EHR records, patient identifiers (`PT-4091`), and clinical trial sites are synthetically generated.
- **Visual & API Disclaimers**: UI header and API response envelopes explicitly display `"Synthetic / Demo Data Only"`.
- **Microsoft Presidio Scrubbing**: Ingestion endpoints run automated PII/PHI redaction regex & NER to purge names, phone numbers, and addresses.

### B. Safe NL2SQL Defense Architecture
- **Read-Only Constraint**: Queries are parsed with `sqlparse` and restricted to `SELECT` statements only.
- **Keyword Blacklist**: Any statement containing `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `EXEC`, or `--` comments is immediately rejected with `400 Bad Request`.
- **Schema Allowlist**: Queries are strictly restricted to `trials`, `patients`, `sites`, and `matches` tables.

### C. Zero Secret Leakage & Key Isolation
- Backend secrets (`SARVAM_API_KEY`, `OPENAI_API_KEY`, `JWT_SECRET_KEY`) reside exclusively in server-side environment variables.
- Secrets are NEVER prefixed with `NEXT_PUBLIC_` and are never serialized into frontend bundles.
- Only `.env.example` with non-functional placeholders is committed to git.
