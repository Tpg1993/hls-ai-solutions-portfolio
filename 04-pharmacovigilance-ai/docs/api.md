# API Specification: AI Pharmacovigilance Platform

Base URL: `http://localhost:8003/api/v1`

## 1. Authentication

### `POST /auth/login`
- **Request Body**: `OAuth2PasswordRequestForm` (`username`, `password`)
- **Response**: JWT token with role claims (`SAFETY_REVIEWER`, `ANALYST`, etc.).

---

## 2. Safety Cases

### `GET /cases`
- **Query Params**: `drug` (string), `severity` (string), `limit` (int)
- **Response**: List of individual case safety reports.

### `POST /cases/extract`
- **RBAC**: Minimum role `ANALYST`.
- **Request Body**:
  ```json
  {
    "narrative": "Patient 58yo female admitted with acute hepatitis after 2 weeks of CardioShield 50mg daily."
  }
  ```
- **Response**: Extracted entities, PII redactions count, and persisted `case_id`.

---

## 3. Signal Intelligence & Evidence

### `GET /signals`
- **Query Params**: `risk_level` (`HIGH`, `MEDIUM`, `LOW`), `status` (`OPEN`, etc.)
- **Response**: List of signals with PRR, ROR, Chi-square, and 95% confidence intervals.

### `GET /signals/{signal_id}/evidence`
- **Response**: List of linked FDA package insert warnings and PubMed publications.

### `POST /signals/{signal_id}/summary`
- **Description**: Synthesizes investigator briefing via Sarvam AI / OpenAI fallback over grounded evidence.

---

## 4. Human Review & Audit

### `POST /reviews`
- **RBAC**: Minimum role `SAFETY_REVIEWER`.
- **Request Body**:
  ```json
  {
    "signal_id": 1,
    "decision": "ESCALATE_LABEL_UPDATE",
    "comments": "Confirmed elevated PRR and literature concordance; escalating to safety committee."
  }
  ```
- **Response**: Persisted review record with sealed timestamp.

### `GET /reviews/audit`
- **RBAC**: Minimum role `AUDITOR`.
- **Response**: List of chronological audit trail events.

---

## 5. Safe NL2SQL

### `POST /nl2sql/query`
- **RBAC**: Minimum role `ANALYST`.
- **Request Body**: `{"question": "Show all high risk signals with PRR > 3.0"}`
- **Response**: Parameterized SQL statement, data rows, and explanation.
