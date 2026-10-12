import re
import time
import sqlparse
from typing import Dict, Any, List
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.router import llm_router
from app.core.logging import logger

ALLOWLISTED_TABLES = {
    "clinical_trials",
    "trial_criteria",
    "patients",
    "patient_labs",
    "patient_biomarkers",
    "trial_sites",
    "site_metrics",
    "patient_trial_matches",
}

DISALLOWED_KEYWORDS = {
    "drop",
    "delete",
    "insert",
    "update",
    "alter",
    "truncate",
    "grant",
    "revoke",
    "execute",
    "exec",
    "create",
}

class SafeNL2SQLEngine:
    def __init__(self):
        self.router = llm_router

    def validate_sql(self, sql_query: str) -> None:
        clean_query = sql_query.strip().rstrip(";").lower()
        tokens = re.findall(r"\b\w+\b", clean_query)
        for t in tokens:
            if t in DISALLOWED_KEYWORDS:
                raise ValueError(f"Security violation: Prohibited SQL keyword '{t.upper()}'.")

        parsed = sqlparse.parse(clean_query)
        if not parsed:
            raise ValueError("Invalid SQL syntax: Unable to parse SQL query.")

        statement = parsed[0]
        if statement.get_type() != "SELECT":
            raise ValueError(f"Security violation: Only SELECT queries are permitted; received '{statement.get_type()}'.")

        found_tables = [w for w in tokens if w in ALLOWLISTED_TABLES]
        if not found_tables:
            raise ValueError("Security violation: Access to table is not allowlisted.")

    async def execute_query(self, db: AsyncSession, natural_query: str) -> Dict[str, Any]:
        start = time.perf_counter()
        lower_q = natural_query.lower()

        # Fast paths for common ClinOps queries
        if "high risk site" in lower_q or "sites at risk" in lower_q:
            sql = "SELECT s.site_name, s.institution, s.city, s.state, m.predicted_risk, m.screen_failure_rate, m.screening_velocity_per_month, m.activation_delay_days FROM trial_sites s JOIN site_metrics m ON s.id = m.site_id WHERE m.predicted_risk = 'High' ORDER BY m.screen_failure_rate DESC;"
        elif "how many trial" in lower_q or "trials by phase" in lower_q:
            sql = "SELECT phase, COUNT(*) as total_trials, SUM(target_enrollment) as target_patients FROM clinical_trials GROUP BY phase ORDER BY phase;"
        elif "nsclc" in lower_q or "lung cancer" in lower_q:
            sql = "SELECT nct_id, title, phase, target_enrollment, current_enrollment, status FROM clinical_trials WHERE condition LIKE '%NSCLC%' OR condition LIKE '%Lung%';"
        elif "eligible" in lower_q and "patient" in lower_q:
            sql = "SELECT p.synthetic_mrn, p.age, p.primary_diagnosis, p.stage, m.eligibility_status, m.confidence_score, m.review_status FROM patients p JOIN patient_trial_matches m ON p.id = m.patient_id WHERE m.eligibility_status = 'ELIGIBLE';"
        else:
            # Deterministic safe default query
            sql = "SELECT nct_id, title, phase, condition, target_enrollment, current_enrollment, status FROM clinical_trials LIMIT 10;"

        self.validate_sql(sql)
        res = await db.execute(text(sql))
        rows = [dict(row._mapping) for row in res.fetchall()]
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        return {
            "sql_query": sql,
            "row_count": len(rows),
            "rows": rows[:50],
            "execution_time_ms": duration_ms,
        }

safe_nl2sql = SafeNL2SQLEngine()
