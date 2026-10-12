import re
import time
import sqlparse
from typing import Dict, Any, List, Tuple
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.router import llm_router
from app.core.logging import logger

ALLOWLISTED_TABLES = {
    "guidance_documents",
    "guidance_sections",
    "submission_impacts",
    "guidance_version_diffs",
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

    async def translate_natural_to_sql(self, natural_query: str) -> str:
        prompt = (
            f"You are a regulatory database SQL expert. Write a clean, safe, read-only SQL query "
            f"compatible with SQLite/PostgreSQL to answer this regulatory affairs question.\n"
            f"{DATABASE_SCHEMA_PROMPT}\n"
            f"USER QUESTION: {natural_query}\n"
            f"CRITICAL RULES:\n"
            f"1. Output ONLY the raw SQL query inside a ```sql ... ``` block.\n"
            f"2. Query ONLY the allowlisted tables.\n"
            f"3. Use UPPERCASE for SQL keywords.\n"
            f"4. Do NOT use any DROP, DELETE, INSERT, UPDATE, or ALTER statements."
        )

        response, _ = await self.router.generate_completion(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=300,
        )

        text_content = response.content
        match = re.search(r"```(?:sql)?(.*?)```", text_content, re.DOTALL | re.IGNORECASE)
        if match:
            sql = match.group(1).strip()
        else:
            lines = [l.strip() for l in text_content.splitlines() if l.strip().upper().startswith("SELECT")]
            sql = lines[0] if lines else text_content.strip()

        return sql

    async def execute_query(self, db: AsyncSession, natural_query: str) -> Dict[str, Any]:
        start = time.perf_counter()
        
        # Rule-based fast paths for common questions
        lower_q = natural_query.lower()
        if "how many guidance" in lower_q or "count of guidance" in lower_q:
            sql = "SELECT authority, COUNT(*) as total_guidances FROM guidance_documents GROUP BY authority ORDER BY total_guidances DESC;"
        elif "critical impact" in lower_q or "high impact" in lower_q:
            sql = "SELECT product_name, ind_nda_number, impact_level, impact_summary, compliance_deadline FROM submission_impacts WHERE impact_level IN ('Critical', 'High') LIMIT 15;"
        elif "fda" in lower_q and ("oncology" in lower_q or "cancer" in lower_q):
            sql = "SELECT title, doc_type, publication_date, version FROM guidance_documents WHERE authority = 'FDA' AND therapeutic_area = 'Oncology' ORDER BY publication_date DESC LIMIT 10;"
        elif "recent" in lower_q or "latest" in lower_q:
            sql = "SELECT authority, title, doc_type, publication_date, version FROM guidance_documents ORDER BY publication_date DESC LIMIT 10;"
        else:
            sql = await self.translate_natural_to_sql(natural_query)

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
