# Data Dictionary & Database Schema: Regulatory Intelligence

## 1. Relational Entities

### Table: `guidance_documents`
Stores regulatory guidance publications from FDA, EMA, and ICH.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto | Guidance record ID |
| `guidance_id` | String | Unique, Indexed | Identifier (e.g., `FDA-2024-D-0192`) |
| `title` | String | Not Null | Guidance title |
| `issuing_body` | String | Indexed | `FDA`, `EMA`, `ICH`, `PMDA` |
| `therapeutic_area`| String | Indexed | `Oncology`, `Immunology`, `Rare Disease`, etc. |
| `status` | String | Not Null | `DRAFT`, `FINAL`, `SUPERSEDED` |
| `publication_date`| String | Not Null | Date of release |
| `summary` | Text | Nullable | Executive regulatory summary |

---

### Table: `diff_analyses`
Stores automated clause-by-clause comparison between guidance revisions.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto | Analysis ID |
| `guidance_id` | String | Indexed | Associated guidance |
| `old_version` | String | Not Null | Baseline revision |
| `new_version` | String | Not Null | Target revision |
| `section_ref` | String | Not Null | Section identifier (e.g., `Section 4.2`) |
| `change_type` | String | Not Null | `ADDED`, `MODIFIED`, `DELETED` |
| `severity` | String | Not Null | `CRITICAL`, `MAJOR`, `MINOR` |
| `old_clause_text`| Text | Nullable | Original clause wording |
| `new_clause_text`| Text | Nullable | Revised clause wording |
| `impact_summary`| Text | Not Null | Clinical/regulatory operational consequence |

---

### Table: `submission_impacts`
Evaluates regulatory changes against specific drug submission dossiers.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto | Impact item ID |
| `program_name` | String | Indexed | Drug development program (e.g., `OncoShield-01`) |
| `dossier_type` | String | Not Null | `NDA`, `BLA`, `IND`, `MAA` |
| `target_module` | String | Not Null | CTD Module (e.g., `Module 2.7 - Clinical Summary`) |
| `action_required`| String | Not Null | `PROTOCOL_AMENDMENT`, `ADDITIONAL_ANALYSIS`, `LABELING_UPDATE` |
| `compliance_deadline`| String | Nullable | Target remediation milestone |
| `status` | String | Default `PENDING_REVIEW` | `PENDING_REVIEW`, `ACCEPTED`, `WAIVED` |
