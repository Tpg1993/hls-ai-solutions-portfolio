# Feature 01: Disproportionality Signal Detection Engine

## 1. Feature Name & Purpose
- **Feature**: Deterministic Statistical Safety Signal Detection (PRR / ROR).
- **Purpose**: Detects statistical disproportionality over incoming spontaneous adverse event streams to flag emerging drug-event safety signals without LLM hallucination.

## 2. User Journey
1. Safety scientist navigates to the **Signal Intelligence** radar.
2. The system calculates 2x2 contingency matrices for all drug-adverse event pairs in real time.
3. Reviewer inspects PRR, ROR, 95% confidence intervals, and Chi-square statistics.
4. Pairs exceeding Evans criteria ($PRR \ge 2.0$, $Obs \ge 3$, $\chi^2 \ge 4.0$) are badged with risk severity tags (`HIGH`, `MEDIUM`).

## 3. RBAC Permissions
- **View Signals**: `STANDARD_USER`, `ANALYST`, `SAFETY_REVIEWER`, `ADMIN`, `SUPER_ADMIN`.
- **Run Signal Detection**: `ANALYST`, `ADMIN`.

## 4. API Endpoints
- `GET /api/v1/signals`
- `GET /api/v1/signals/{signal_id}`

## 5. Statistical Algorithms
- Proportional Reporting Ratio: $PRR = \frac{a / (a + b)}{c / (c + d)}$
- Reporting Odds Ratio: $ROR = \frac{a \times d}{b \times c}$
- Chi-Square with Yates continuity correction.
