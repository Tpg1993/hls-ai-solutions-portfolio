# Data Dictionary & Database Schema

## 1. Relational Entities (SQLite / PostgreSQL)

### Table: `trials`
Stores synthetic clinical trial protocol specifications.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto | Internal trial identifier |
| `nct_id` | String | Unique, Indexed | Synthetic NCT protocol ID (e.g., `NCT05912345`) |
| `title` | String | Not Null | Protocol title |
| `phase` | String | Not Null | Phase (e.g., `Phase I`, `Phase II`, `Phase III`) |
| `indication` | String | Indexed | Disease indication (e.g., `NSCLC`, `Melanoma`, `CRC`) |
| `target_accrual` | Integer | Not Null | Planned total enrollment target |
| `current_enrolled`| Integer| Default 0 | Current recruited patients |
| `status` | String | Not Null | `RECRUITING`, `ACTIVE_NOT_RECRUITING`, `COMPLETED` |
| `inclusion_criteria` | JSON | Not Null | Array of inclusion rules with thresholds and operators |
| `exclusion_criteria` | JSON | Not Null | Array of exclusion rules with washout windows |

---

### Table: `patients`
Synthetic oncology patient electronic health records (EHR).
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto | Internal patient record ID |
| `patient_code` | String | Unique, Indexed | De-identified ID (e.g., `PT-4091`) |
| `age` | Integer | Not Null | Patient chronological age |
| `gender` | String | Not Null | Gender (`M`, `F`, `Other`) |
| `diagnosis` | String | Indexed | Primary histological diagnosis |
| `stage` | String | Not Null | Cancer stage (e.g., `Stage IV`, `Stage IIIB`) |
| `ecog_ps` | Integer | Not Null | ECOG Performance Status (0 to 4) |
| `biomarkers` | JSON | Not Null | Mutation status (e.g., `{"EGFR": "L858R", "KRAS": "G12D", "PD-L1": "65%"}`) |
| `labs` | JSON | Not Null | Recent lab panels (e.g., `{"platelets": 145000, "creatinine": 1.1, "anc": 2100}`) |
| `prior_therapies` | JSON | Not Null | Previous drug regimens and stop dates |

---

### Table: `trial_sites`
Clinical research sites executing trials.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto | Site identifier |
| `trial_id` | Integer | FK (`trials.id`) | Trial linked to this site |
| `site_name` | String | Not Null | Institution name (e.g., `Dana-Farber Cancer Institute`) |
| `country` | String | Not Null | Geographical location (`US`, `DE`, `UK`, `JP`) |
| `planned_target` | Integer | Not Null | Target enrollment milestone |
| `actual_enrolled`| Integer | Not Null | Current enrolled count |
| `screening_velocity` | Float | Not Null | Patients screened per month |
| `screen_failure_rate` | Float | Not Null | Ratio of screened patients failing eligibility |
| `crc_turnover_rate` | Float | Not Null | Coordinator turnover rate (operational friction index) |
| `risk_score` | Float | Computed | XGBoost risk score [0.0 - 1.0] |
| `risk_level` | String | Computed | `LOW`, `MEDIUM`, `HIGH` |

---

### Table: `clinical_reviews`
Immutable human-in-the-loop decision trail for clinical reviewers.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto | Review record ID |
| `patient_id` | Integer | FK (`patients.id`) | Patient evaluated |
| `trial_id` | Integer | FK (`trials.id`) | Protocol evaluated |
| `reviewer_id` | Integer | FK (`users.id`) | Reviewer who signed off |
| `decision` | String | Not Null | `APPROVED`, `REJECTED`, `FLAGGED_FOR_FOLLOWUP` |
| `justification` | Text | Not Null | Clinical notes and protocol reasoning |
| `criterion_matrix_snapshot` | JSON | Not Null | Snapshot of PASS/FAIL/UNKNOWN evaluation at decision time |
| `created_at` | DateTime | Timestamp | Sealed timestamp of review sign-off |
