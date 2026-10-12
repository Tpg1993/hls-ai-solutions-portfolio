# Data Dictionary & Database Schema: Pharmacovigilance

## 1. Tables Overview

### Table: `safety_cases`
Stores individual case safety reports (ICSRs).
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto | Internal identifier |
| `case_id` | String | Unique, Indexed | ICSR identifier (e.g., `ICSR-2026-1004`) |
| `age` | Integer | Nullable | Patient age |
| `sex` | String | Nullable | Patient sex (`M`, `F`) |
| `suspect_drug` | String | Indexed | Suspect pharmaceutical product |
| `dosage` | String | Nullable | Administered dose regimen |
| `adverse_event`| String | Indexed | Reported adverse event |
| `meddra_soc` | String | Indexed | MedDRA System Organ Class |
| `severity` | String | Indexed | `SERIOUS_HOSPITALIZATION`, `LIFE_THREATENING`, `NON_SERIOUS` |
| `outcome` | String | Nullable | `RECOVERED`, `NOT_RECOVERED`, `FATAL`, `UNKNOWN` |
| `country` | String | Nullable | Country of origin |
| `narrative_scrubbed`| Text | Nullable | Anonymized case description |

---

### Table: `safety_signals`
Stores computed disproportionality metrics for drug-event pairs.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto | Signal ID |
| `drug_name` | String | Indexed | Drug name |
| `adverse_event` | String | Indexed | Target adverse event |
| `observed_cases`| Integer | Not Null | Observed cases ($a$) |
| `expected_cases`| Float | Not Null | Expected cases under independence ($E$) |
| `prr` | Float | Not Null | Proportional Reporting Ratio |
| `prr_ci_lower` | Float | Not Null | Lower bound 95% CI |
| `prr_ci_upper` | Float | Not Null | Upper bound 95% CI |
| `ror` | Float | Not Null | Reporting Odds Ratio |
| `chi_square` | Float | Not Null | Chi-square statistic with Yates correction |
| `risk_level` | String | Default `MEDIUM` | Risk tier: `HIGH`, `MEDIUM`, `LOW` |
| `signal_status` | String | Default `OPEN` | `OPEN`, `INVESTIGATING`, `CLOSED`, `ESCALATED_LABEL_UPDATE` |

---

### Table: `evidence_documents`
Stores product label text chunks and PubMed literature abstracts.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto | Document ID |
| `doc_type` | String | Not Null | `DRUG_LABEL` or `LITERATURE_PUBMED` |
| `drug_name` | String | Indexed | Associated drug name |
| `title` | String | Not Null | Publication / Section title |
| `citation` | String | Nullable | Regulatory or PubMed reference |
| `text_chunk` | Text | Not Null | Evidence snippet |

---

### Table: `safety_reviews`
Immutable sign-off decisions by drug safety reviewers.
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto | Review record ID |
| `signal_id` | Integer | FK (`safety_signals.id`) | Signal reviewed |
| `reviewer_username`| String | Not Null | Reviewing physician |
| `decision` | String | Not Null | `ESCALATE_LABEL_UPDATE`, `CONTINUE_ROUTINE_SURVEILLANCE`, `DISMISS_SIGNAL` |
| `comments` | Text | Not Null | Clinical justification |
| `snapshot_prr` | Float | Not Null | Signal PRR at decision time |
| `created_at` | DateTime | Timestamp | Timestamp of sign-off |
