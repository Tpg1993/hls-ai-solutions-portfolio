# Feature 01: Automated Patient-Trial Eligibility Matching

## 1. Feature Name & Purpose
- **Feature**: Patient-Trial Genomic and Biomarker Eligibility Screening Engine
- **Purpose**: Automates the complex screening of oncology patients against multi-arm clinical trial protocols (e.g. EGFR Exon 20 insertion, HER2 IHC 3+, T790M) using deterministic rule logic paired with Sarvam AI clinical narrative justification.
- **Target Personas**: Clinical Research Coordinators (CRCs), Principal Investigators (PIs), Clinical Reviewers.

## 2. User Journey
1. Clinical Reviewer opens the Trial Intelligence dashboard and selects an active trial (e.g. NCT04488081 - CHRYSALIS-2 or NCT03329092 - DESTINY-Breast03).
2. The system queries EHR patient profiles (labs, histology, NGS gene alterations, prior lines of therapy).
3. The deterministic eligibility engine runs hard inclusion/exclusion gates (ECOG status, organ function labs, biomarker alignment).
4. For matched or borderline patients, Sarvam AI synthesizes an audit-ready Clinical Screening Summary citing specific protocol criteria.
5. Reviewer inspects the biomarker alignments and approves or excludes the candidate with human sign-off.

## 3. RBAC Permissions
- `CLINICAL_REVIEWER` (Level 40) or higher: Run screening, view clinical justifications, approve/reject matches.
- `AUDITOR` (Level 20): Read-only view of screening histories and audit logs.

## 4. API Endpoints
- `GET /api/v1/trials`: List active clinical trial protocols with arms and phases.
- `POST /api/v1/screening/evaluate`: Deterministic protocol evaluation between patient and trial.
- `POST /api/v1/screening/ai-summary`: Sarvam AI clinical rationale synthesis.

## 5. Data & ML Models
- **Protocol Data**: Real clinical identifiers (NCT04488081, NCT03329092, NCT04077099) with real inclusion/exclusion parameters.
- **Biomarker Features**: Genomic alterations (EGFR, ERBB2/HER2, KRAS, ALK, ROS1), lab thresholds (ANC, Platelets, CrCl, AST/ALT, LVEF).
- **LLM**: Sarvam AI (`sarvam-105b-conversations`) with OpenAI fallback for grounded narrative reasoning.

## 6. Error & Edge States
- Missing genomic panel: Marked as "Biomarker Unknown" with cautionary status.
- Lab value out of bounds: Highlighted in red with specific threshold deficit (e.g. CrCl < 50 mL/min).
- LLM Provider Failure: Automatic fallback to OpenAI or deterministic fallback summary without workflow disruption.

## 7. Testing Strategy
- Unit tests: [test_clinical_api.py](../../backend/tests/integration/test_clinical_api.py) validates criteria logic and schema compliance.
- E2E tests: Playwright & Selenium browser validation for trial switching and patient screening cards.
