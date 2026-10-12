# Feature 03: Human-in-the-Loop Clinical Review Workflow

## 1. Feature Name & Purpose
- **Feature**: Human-in-the-Loop (HITL) Patient Eligibility Sign-off & Audit Trail
- **Purpose**: Enforces mandatory clinical investigator review before any patient is enrolled or referred to an investigational trial arm, ensuring regulatory compliance and patient safety.
- **Target Personas**: Principal Investigators (PIs), Sub-Investigators, Clinical Research Coordinators.

## 2. User Journey
1. Clinical Reviewer navigates to "Review Queue".
2. System presents AI-screened candidates with eligibility status (ELIGIBLE, INELIGIBLE, REVIEW_REQUIRED).
3. Reviewer inspects lab values, ECOG score, and Sarvam AI screening justifications.
4. Reviewer clicks "Approve for Enrollment" or "Disqualify Candidate", optionally entering clinical notes.
5. Action is recorded with timestamp, reviewer ID, and cryptographic audit hash in the review history.

## 3. RBAC Permissions
- `CLINICAL_REVIEWER` (Level 40) or `ADMIN` (Level 80): Mandatory for submitting eligibility decisions.
- Read-only roles cannot modify review status.

## 4. API Endpoints
- `GET /api/v1/matches/pending`: Retrieve pending screening reviews.
- `POST /api/v1/matches/{id}/review`: Submit approval or rejection with clinical justification.

## 5. Data & Audit Trail
- Records: Patient ID, Trial ID, Prior Status, New Status, Reviewer ID, Timestamp, Clinical Notes.
- Immutability: Review events cannot be deleted or overwritten via the API.

## 6. Testing Strategy
- Pytest API tests verify role enforcement (`CLINICAL_REVIEWER` allowed, `STANDARD_USER` rejected with 403 Forbidden).
- Audit trail integrity verified via end-to-end status change sequence.
