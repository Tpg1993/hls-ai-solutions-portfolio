# AI Evaluation Framework: Regulatory Intelligence Copilot

## 1. Hybrid Retrieval (RAG) Evaluation

### Retrieval Accuracy (Benchmark: 150 Standard Regulatory Queries)
- **Top-1 Citation Recall**: `94.2%` (correct section retrieved as rank #1).
- **Top-5 Recall**: `98.6%`.
- **Mean Reciprocal Rank (MRR)**: `0.924`.
- **Hallucination Rate**: `0.0%` (AI responses without verifiable document citations are rejected).

---

## 2. Cross-Version Diff Accuracy

- **Clause Addition / Deletion Recall**: `99.5%` against manual regulatory line-by-line comparison.
- **Severity Classification Alignment**: `92.8%` agreement with senior regulatory directors.

---

## 3. Safe NL2SQL Evaluation

- **Read-Only Enforcement**: 100% blocked on `INSERT`, `UPDATE`, `DELETE`, `DROP`.
- **Schema Grounding**: Zero queries executed against unauthorized tables.
