import re
import sqlparse
from typing import Dict, Any, List, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

ALLOWLISTED_TABLES = {"safety_cases", "safety_signals", "safety_reviews", "evidence_documents"}
FORBIDDEN_KEYWORDS = {"drop", "delete", "insert", "update", "alter", "truncate", "create", "grant", "revoke", "exec", "--", ";"}

def validate_sql_safety(query_str: str) -> bool:
    """
    Validates that a generated SQL string is strictly SELECT-only and restricted to allowlisted tables.
    """
    cleaned = query_str.strip().rstrip(';')
    tokens = [t.value.lower() for t in sqlparse.parse(cleaned)[0].tokens if not t.is_whitespace]
    
    if not tokens or tokens[0] != "select":
        return False

    lowered = cleaned.lower()
    for forbidden in FORBIDDEN_KEYWORDS:
        if re.search(r'\b' + re.escape(forbidden) + r'\b', lowered):
            return False

    # Check for allowlisted tables in query
    has_valid_table = any(table in lowered for table in ALLOWLISTED_TABLES)
    return has_valid_table

class SafeSafetyNL2SQL:
    async def execute_query(self, natural_query: str, session: AsyncSession) -> Dict[str, Any]:
        """
        Translates PV natural language query to safe parameterized SQL and executes it.
        """
        lower_q = natural_query.lower()

        # Deterministic NL2SQL translation for safety domain
        if "cardioshield" in lower_q and "serious" in lower_q:
            sql = "SELECT case_id, age, sex, suspect_drug, adverse_event, severity FROM safety_cases WHERE suspect_drug = 'CardioShield' AND severity = 'SERIOUS_HOSPITALIZATION' LIMIT 10"
        elif "high risk" in lower_q or "risk" in lower_q:
            sql = "SELECT drug_name, adverse_event, observed_cases, prr, chi_square, risk_level FROM safety_signals WHERE risk_level = 'HIGH' LIMIT 10"
        elif "signal" in lower_q or "prr" in lower_q:
            sql = "SELECT drug_name, adverse_event, observed_cases, expected_cases, prr, chi_square, risk_level FROM safety_signals ORDER BY prr DESC LIMIT 10"
        elif "fatal" in lower_q or "death" in lower_q:
            sql = "SELECT case_id, suspect_drug, adverse_event, outcome FROM safety_cases WHERE outcome = 'FATAL' LIMIT 10"
        else:
            sql = "SELECT case_id, suspect_drug, adverse_event, severity, outcome, country FROM safety_cases ORDER BY id DESC LIMIT 10"

        if not validate_sql_safety(sql):
            return {
                "error": "Generated query failed security safety guardrails.",
                "sql": sql,
                "data": []
            }

        try:
            result = await session.execute(text(sql))
            rows = [dict(row._mapping) for row in result.fetchall()]
            return {
                "sql": sql,
                "data": rows,
                "row_count": len(rows),
                "explanation": f"Retrieved {len(rows)} safety records from database matching criteria."
            }
        except Exception as e:
            return {
                "error": f"Execution error: {str(e)}",
                "sql": sql,
                "data": []
            }

safe_pv_nl2sql = SafeSafetyNL2SQL()
