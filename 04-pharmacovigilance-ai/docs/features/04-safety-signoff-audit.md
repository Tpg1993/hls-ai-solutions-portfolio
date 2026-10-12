# Feature 04: Human-in-the-Loop Safety Sign-Off & Audit Trail

## 1. Feature Name & Purpose
- **Feature**: Safety Physician Review Gate & Cryptographic Audit Log.
- **Purpose**: Enforces mandatory clinical sign-off by a qualified Safety Reviewer (`SAFETY_REVIEWER`) before signal escalation or dismissal, maintaining full FDA 21 CFR Part 11 audit compliance.

## 2. User Journey
1. Safety Physician opens the **Safety Committee Sign-Off** workstation.
2. Selects disposition action:
   - `ESCALATE_LABEL_UPDATE`
   - `CONTINUE_ROUTINE_SURVEILLANCE`
   - `REQUEST_INVESTIGATOR_MEETING`
   - `DISMISS_SIGNAL`
3. Inputs medical rationale and literature concordance notes.
4. Submits decision; signal status is permanently updated and audit event is recorded.
5. Compliance auditors inspect the immutable chronological audit log.

## 3. RBAC Permissions
- **Submit Decision**: `SAFETY_REVIEWER`, `ADMIN`, `SUPER_ADMIN`.
- **Inspect Audit Trail**: `AUDITOR`, `ADMIN`, `SUPER_ADMIN`.

## 4. API Endpoints
- `POST /api/v1/reviews`
- `GET /api/v1/reviews/audit`
