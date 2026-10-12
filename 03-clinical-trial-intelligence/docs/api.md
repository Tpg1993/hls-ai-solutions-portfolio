# API Specification: Clinical Trial Intelligence

Base URL: `http://localhost:8002/api/v1`

## 1. Authentication Endpoints

### `POST /auth/login`
- **Request Body**: `OAuth2PasswordRequestForm` (`username`, `password`)
- **Response**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "role": "CLINICAL_REVIEWER",
    "username": "clinops_lead"
  }
  ```

---

## 2. Trials & Patients

### `GET /trials`
- **Query Params**: `indication` (string), `phase` (string), `limit` (int)
- **Response**: List of clinical trials including target accrual and criteria.

### `GET /patients`
- **Query Params**: `diagnosis` (string), `stage` (string), `limit` (int)
- **Response**: List of synthetic de-identified oncology patient profiles.

---

## 3. Patient Matching & Verification

### `POST /matching/evaluate`
- **Description**: Evaluates eligibility of a patient against trial protocol inclusion/exclusion criteria.
- **Request Body**:
  ```json
  {
    "patient_id": 1,
    "trial_id": 2
  }
  ```
- **Response**:
  ```json
  {
    "patient_code": "PT-4091",
    "trial_nct_id": "NCT05912345",
    "overall_status": "ELIGIBLE",
    "overall_score": 0.94,
    "criteria_evaluations": [
      {
        "criterion_id": "INC-01",
        "description": "Age >= 18 years at time of informed consent",
        "status": "PASS",
        "evidence": "Patient is 54 years old",
        "category": "INCLUSION"
      },
      {
        "criterion_id": "EXC-03",
        "description": "Active brain metastases",
        "status": "PASS",
        "evidence": "No neurological symptoms or CNS metastases reported",
        "category": "EXCLUSION"
      }
    ],
    "missing_biomarkers": []
  }
  ```

---

## 4. Site Operational Risk & Forecasting

### `GET /sites/risk-forecast`
- **Query Params**: `trial_id` (optional int)
- **Response**: List of trial sites with operational metrics and XGBoost risk forecast (`LOW`, `MEDIUM`, `HIGH`).

---

## 5. ClinOps Safe NL2SQL

### `POST /nl2sql/query`
- **Description**: Natural language question answering over trial and site database.
- **Request Body**:
  ```json
  {
    "question": "Which trial sites have a screen failure rate greater than 40%?"
  }
  ```
- **Response**:
  ```json
  {
    "generated_sql": "SELECT site_name, country, screen_failure_rate FROM trial_sites WHERE screen_failure_rate > 0.40;",
    "results": [
      {"site_name": "Memorial University Hospital", "country": "US", "screen_failure_rate": 0.48}
    ],
    "explanation": "Found 1 site exceeding the 40% screen failure threshold."
  }
  ```

---

## 6. Clinical Reviewer Sign-Off

### `POST /matching/review`
- **RBAC Guard**: Requires role `CLINICAL_REVIEWER`, `ADMIN`, or `SUPER_ADMIN`.
- **Request Body**:
  ```json
  {
    "match_evaluation_id": 104,
    "decision": "APPROVED",
    "justification": "Verified EGFR exon 20 insertion and required 4-week washout confirmed."
  }
  ```
- **Response**:
  ```json
  {
    "status": "SUCCESS",
    "audit_event_id": 512,
    "timestamp": "2026-10-12T05:35:00Z"
  }
  ```
