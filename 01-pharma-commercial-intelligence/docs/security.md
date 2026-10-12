# Security Architecture & Compliance Guidelines

## 1. Zero Secrets in Version Control
- All credentials reside exclusively in `.env` (ignored by `.gitignore`).
- Only `.env.example` with non-functional placeholders is tracked in Git.
- Provider API keys (`SARVAM_API_KEY`, `OPENAI_API_KEY`) are backend-only. Never expose keys with `NEXT_PUBLIC_` prefixes.

## 2. Server-Side Role-Based Access Control (RBAC)
Authorization is strictly enforced in FastAPI via dependency injection:
- `SUPER_ADMIN` (100): System and tenant administration.
- `ADMIN` (80): User management, batch recommendation triggers.
- `BUSINESS_OWNER` (60): ROI parameters, commercial analytics.
- `ANALYST` (40): HCP drilldown, AI explanation runs, NL2SQL queries.
- `AUDITOR` (20): Read-only access to immutable audit trail.
- `STANDARD_USER` (10): Directory viewing and high-level charts.

## 3. Presidio PII/PHI Sanitization
All free-text queries are scrubbed of person names, email addresses, and phone numbers before being dispatched to external LLMs.

## 4. Safe NL2SQL AST Validation
- Queries restricted to `SELECT` operations only.
- Prohibited tokens: `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `EXEC`.
- Table allowlisting: `hcps`, `prescriptions`, `products`, `territories`, `interactions`, `recommendations`.
- Strict query execution timeout (3 seconds) and row limits (`LIMIT 100`).
