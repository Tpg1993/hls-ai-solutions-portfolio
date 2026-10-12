# Feature: Safe NL2SQL Commercial Explorer

## 1. Purpose & Business Context
Enables commercial operations directors and analysts to query longitudinal datasets using natural language questions (e.g. *"Show me all oncologists in District 1 with >30 competitor prescriptions"*).

## 2. Security Guardrails & AST Validation
- **Read-Only**: Restricts queries to `SELECT` statements via `sqlparse`.
- **Keyword Blocking**: Forbids `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `EXEC`.
- **Table Allowlisting**: Restricts access to `hcps`, `prescriptions`, `products`, `territories`, `interactions`, and `recommendations`.
- **Query Bounds**: Imposes query timeouts (3s) and row bounds (`LIMIT 100`).

## 3. RBAC Permissions
- Required Role: `ANALYST` or higher.
- API Endpoint: `POST /api/ai/nl2sql`.
