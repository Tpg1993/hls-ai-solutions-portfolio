# Feature 02: Automated Cross-Version Regulatory Diff Analyzer

## 1. Feature Name & Purpose
- **Feature Name**: Cross-Version Semantic Diff Analyzer
- **Purpose**: Automates side-by-side comparison between draft vs. final guidance iterations (e.g. FDA RWE Draft 2021 vs Final 2024, ICH E6(R2) vs E6(R3)), identifying structural additions, deletions, modifications, and assigning compliance impact severity (`CRITICAL`, `HIGH`, `MEDIUM`).

## 2. User Journey
1. Submissions Lead navigates to **Version Diff**.
2. Selects baseline document (`DOC-FDA-RWE-2021`) and comparison document (`DOC-FDA-RWE-2024`).
3. System visualizes side-by-side clause changes with red/green highlights and Sarvam AI synthesized regulatory impact summaries.
4. Lead identifies that FDA added a mandatory 15% independent source data verification requirement and quantitative E-value sensitivity testing.

## 3. RBAC Permissions
- Minimum Role: `STANDARD_USER` (Level 10) to view diffs; `REGULATORY_REVIEWER` (Level 40) to export regulatory memos.

## 4. API Endpoints
- `GET /api/diff/compare?baseline_id={id}&comparison_id={id}`: Returns structured diff breakdown and severity counts.
