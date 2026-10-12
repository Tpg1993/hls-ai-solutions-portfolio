# Feature 02: Case Narrative Intake & Entity Extraction

## 1. Feature Name & Purpose
- **Feature**: Automated ICSR Narrative Processing & PII Scrubbing.
- **Purpose**: Ingests unstructured clinical case narratives, redacts patient PII/PHI, and parses structured MedDRA entities and severity grades.

## 2. User Journey
1. Safety Case Specialist enters raw narrative text.
2. System redacts phone numbers, emails, and identifiers into tokens like `[REDACTED_PHONE]`.
3. Entity extractor isolates suspect drug, MedDRA adverse event, System Organ Class, age, sex, and hospitalization severity.
4. Record is saved to `safety_cases` table and logged in the audit trail.

## 3. RBAC Permissions
- **Execute Extraction & Save**: `ANALYST`, `ADMIN`, `SUPER_ADMIN`.

## 4. API Endpoints
- `POST /api/v1/cases/extract`
- `GET /api/v1/cases`
