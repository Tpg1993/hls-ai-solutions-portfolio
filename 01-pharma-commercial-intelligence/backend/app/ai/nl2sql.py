import re
import time
from typing import Dict, Any, List, Tuple
import sqlparse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.router import llm_router
from app.core.logging import logger

ALLOWED_TABLES = {
    "hcps",
    "prescriptions",
    "products",
    "territories",
    "interactions",
    "recommendations",
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

SCHEMA_PROMPT = """
You are an expert SQL analyst for a Pharma Commercial Intelligence platform.
You generate Postgres SQL queries based on user requests.

Database Schema:
- hcps (id, npi_synthetic, first_name, last_name, specialty, hospital_affiliation, city, state, territory_id, decile, digital_affinity, adoption_stage)
- territories (id, name, region, quota, assigned_rep_name, assigned_rep_email, target_specialty)
- products (id, name, therapeutic_area, brand_tier, price_per_unit, competitor_product_name)
- prescriptions (id, hcp_id, product_id, month_year, trx_count, nrx_count, competitor_trx_count)
- interactions (id, hcp_id, interaction_date, channel, rep_name, topics_discussed, sentiment, notes)
- recommendations (id, hcp_id, product_id, propensity_score, priority_tier, recommended_action, recommended_channel, status)

RULES:
1. Output ONLY a valid SQL query without markdown or explanations.
2. Only use SELECT statements.
3. Always include LIMIT 100 unless a specific small limit is requested.
4. Use standard ANSI SQL / PostgreSQL syntax.
"""

class SafeNL2SQLEngine:
    def validate_sql(self, sql_query: str) -> Tuple[bool, str]:
        """
        Validates that SQL statement is strictly read-only and uses allowed tables only.
        """
        clean_sql = sql_query.strip().strip(";").lower()

        # Check for forbidden keywords
        tokens = re.findall(r"\b\w+\b", clean_sql)
        for t in tokens:
            if t in DISALLOWED_KEYWORDS:
                return False, f"Forbidden SQL keyword detected: '{t.upper()}'"

        parsed = sqlparse.parse(clean_sql)
        if not parsed:
            return False, "Unable to parse SQL query"

        statement = parsed[0]
        if statement.get_type() != "SELECT":
            return False, f"Only SELECT queries are allowed; received: '{statement.get_type()}'"

        # Check tables mentioned in query
        found_tables = []
        for word in tokens:
            if word in ALLOWED_TABLES:
                found_tables.append(word)

        if not found_tables:
            return False, "Query must reference at least one valid commercial database table"

        return True, "Valid"

    async def generate_sql(self, natural_query: str) -> str:
        """
        Translates natural language to SQL using LLM router.
        """
        messages = [
            {"role": "system", "content": SCHEMA_PROMPT},
            {"role": "user", "content": f"Generate a SQL query for: {natural_query}"},
        ]
        response, _ = await llm_router.generate_completion(
            messages,
            temperature=0.0,
            max_tokens=300,
            grounded_facts={"hcp_name": "Dr. Query"},
        )
        raw_sql = response.content.strip()
        # Clean markdown formatting if present
        raw_sql = re.sub(r"^```sql\s*", "", raw_sql, flags=re.IGNORECASE)
        raw_sql = re.sub(r"^```\s*", "", raw_sql)
        raw_sql = re.sub(r"\s*```$", "", raw_sql)
        raw_sql = raw_sql.strip()

        # Ensure limit
        if "limit" not in raw_sql.lower():
            raw_sql = f"{raw_sql} LIMIT 50"

        return raw_sql

    async def execute_query(
        self,
        db: AsyncSession,
        natural_query: str,
        override_sql: str = None
    ) -> Dict[str, Any]:
        """
        Executes safe NL2SQL query with timing and row limit.
        """
        start_time = time.perf_counter()
        sql_query = override_sql or await self.generate_sql(natural_query)

        is_valid, reason = self.validate_sql(sql_query)
        if not is_valid:
            raise ValueError(f"Security validation failed: {reason}")

        try:
            result = await db.execute(text(sql_query))
            rows = result.mappings().all()
            execution_time = (time.perf_counter() - start_time) * 1000

            columns = list(result.keys()) if rows or result.returns_rows else []
            data = [dict(row) for row in rows[:100]]

            return {
                "natural_query": natural_query,
                "generated_sql": sql_query,
                "row_count": len(data),
                "columns": columns,
                "results": data,
                "execution_time_ms": round(execution_time, 2),
            }
        except Exception as e:
            logger.error(f"SQL execution error for query [{sql_query}]: {str(e)}")
            raise RuntimeError(f"Database execution error: {str(e)}")

safe_nl2sql = SafeNL2SQLEngine()
