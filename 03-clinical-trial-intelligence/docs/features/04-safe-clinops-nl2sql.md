# Feature 04: Safe Natural Language to SQL (NL2SQL) Engine

## 1. Feature Name & Purpose
- **Feature**: Enterprise Safe Natural Language SQL Query Engine for Clinical Operations
- **Purpose**: Enables clinical leads and study planners to query protocol enrollment, site capacity, and patient demographics in natural English with strict SQL security controls.
- **Target Personas**: Clinical Data Managers, Biostatisticians, Clinical Study Directors.

## 2. User Journey
1. User enters natural language questions in the ClinOps Copilot (e.g., "Which clinical trials are in Phase 3?", "List patients with ECOG score <= 1").
2. Engine maps intent to safe parameterized SQL against the relational clinical schema (`trials`, `patients`, `sites`, `patient_matches`).
3. Security validator blocks any DDL/DML, multi-statement injection, or unauthorized table access.
4. Engine executes query read-only and returns tabular results with interactive chart visualization and AI interpretation.

## 3. RBAC Permissions
- `ANALYST`, `CLINICAL_REVIEWER`, `ADMIN`, `SUPER_ADMIN`: Authorized to run safe queries.
- `STANDARD_USER`: Restricted to predefined canned queries.

## 4. API Endpoints
- `POST /api/v1/query/nl2sql`: Translates natural language into verified SQL and executes against database.

## 5. Security & Safety Gates
- **Read-Only Enforced**: Only `SELECT` statements are executed.
- **Table Allowlist**: Only `trials`, `patients`, `sites`, and `patient_matches` can be queried.
- **Syntax Validation**: Validated via AST parser (`sqlparse`) before execution.
- **No Direct Table Mutation**: `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER` are immediately rejected with 400 Bad Request.

## 6. Testing Strategy
- Unit tests verify rejection of dangerous SQL commands (`DROP TABLE`, `INSERT INTO`, comments `--`, stacked queries `;`).
- Valid query generation tests verify correct table joins and aggregations.
