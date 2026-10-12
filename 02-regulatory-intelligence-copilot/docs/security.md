# Security & RBAC Governance: Regulatory Intelligence Copilot

## 1. Role-Based Access Control (RBAC) Matrix

Authorization is strictly enforced in the FastAPI backend via route dependencies (`app.core.security.require_role`). Default policy is **Deny by Default**.

| Role | Level | Permissions | Scope |
| :--- | :---: | :--- | :--- |
| **SUPER_ADMIN** | 100 | System settings, user provisioning, global telemetry | Full system administration |
| **ADMIN** | 80 | Guidance upload, index re-building, cache flushing | Operational administration |
| **REGULATORY_REVIEWER** | 60 | Sign off submission impact matrices, verify citations | Regulatory decision trail |
| **ANALYST** | 40 | Execute hybrid searches, run version diffs, query safe NL2SQL | Regulatory research |
| **AUDITOR** | 20 | Read-only inspection of immutable regulatory compliance logs | Compliance inspection |
| **STANDARD_USER** | 10 | Read-only view of public guidance summaries | Basic browsing |

---

## 2. Threat Modeling & Defense Strategies

### A. Grounded Citations & Hallucination Prevention
- The AI summarizer is strictly grounded on retrieved guidance excerpts.
- If retrieved evidence is insufficient to answer a regulatory query, the system explicitly responds: *"Insufficient regulatory guidance found in catalog."*

### B. Safe Read-Only NL2SQL
- AST validation via `sqlparse`: Only `SELECT` statements permitted.
- Reject any attempt containing `DROP`, `DELETE`, `INSERT`, `UPDATE`, `ALTER`, `TRUNCATE`, `EXEC`.
- Table allowlisting restricted to `guidance_documents`, `guidance_versions`, `diff_analyses`, and `submission_impacts`.

### C. Zero Secret Leakage
- LLM API keys (`SARVAM_API_KEY`, `OPENAI_API_KEY`) and JWT secrets reside exclusively in backend environment variables.
- No provider keys are exposed to the frontend browser bundle.
