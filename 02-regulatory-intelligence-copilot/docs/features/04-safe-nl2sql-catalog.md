# Feature 04: Safe Regulatory NL2SQL Metadata Explorer

## 1. Feature Name & Purpose
- **Feature Name**: Safe NL2SQL Regulatory Metadata Explorer
- **Purpose**: Allows analysts and compliance directors to query regulatory databases using natural language, safely generating read-only parameterized SQL queries with AST security validation.

## 2. User Journey
1. Analyst navigates to **NL2SQL Explorer**.
2. Types natural query: *"How many guidances are published by each authority?"* or selects a quick preset.
3. System translates intent to read-only SQL, verifies against table allowlists (`guidance_documents`, `submission_impacts`, etc.), executes query safely, and renders formatted tabular results with execution latency.

## 3. RBAC Permissions
- Minimum Role: `REGULATORY_REVIEWER` (Level 40).

## 4. API Endpoints
- `POST /api/nl2sql`: Accepts `{ query }`, returns generated SQL, row count, execution time, and records.
