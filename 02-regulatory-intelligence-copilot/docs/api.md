# API Specification: Regulatory Intelligence Copilot

Base URL: `http://localhost:8001/api/v1`

## 1. Authentication

### `POST /auth/login`
- **Request Body**: `OAuth2PasswordRequestForm` (`username`, `password`)
- **Response**: JWT token with role claims (`REGULATORY_REVIEWER`, `ANALYST`, etc.).

---

## 2. Regulatory Guidance Catalog & Search

### `GET /guidance`
- **Query Params**: `therapeutic_area` (string), `issuing_body` (`FDA`, `EMA`, `ICH`), `limit` (int)
- **Response**: List of regulatory guidance documents.

### `POST /guidance/search`
- **Description**: Hybrid keyword + vector semantic search with citation extraction.
- **Request Body**:
  ```json
  {
    "query": "accelerated approval surrogate endpoints in NSCLC",
    "top_k": 5
  }
  ```
- **Response**: Ranked regulatory snippets, document references, and citation metadata.

---

## 3. Cross-Version Diff Engine

### `GET /diffs`
- **Query Params**: `guidance_id` (string), `severity` (`CRITICAL`, `MAJOR`, `MINOR`)
- **Response**: List of added, modified, or deleted clauses between guidance versions.

---

## 4. Submission Impact Matrix

### `GET /submissions/impact-matrix`
- **Query Params**: `program_name` (optional string)
- **Response**: CTD modules affected by guidance changes, required actions, and deadlines.

### `POST /submissions/impact-matrix/signoff`
- **RBAC**: Requires role `REGULATORY_REVIEWER` or `ADMIN`.
- **Request Body**:
  ```json
  {
    "impact_id": 4,
    "decision": "ACCEPTED",
    "notes": "Protocol amendment approved for inclusion in upcoming Module 5 sequence."
  }
  ```

---

## 5. Safe NL2SQL

### `POST /nl2sql/query`
- **RBAC**: Minimum role `ANALYST`.
- **Request Body**: `{"question": "Show all critical version changes published by FDA in 2024"}`
- **Response**: Parameterized safe SQL statement, execution rows, and explanation.
