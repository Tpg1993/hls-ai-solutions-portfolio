import pytest
from app.ai.nl2sql import safe_nl2sql

def test_nl2sql_allowlisted_query():
    safe_nl2sql.validate_sql("SELECT nct_id, title, phase, status FROM clinical_trials WHERE phase = 'Phase 2';")

def test_nl2sql_prohibited_drop():
    with pytest.raises(ValueError, match="Security violation"):
        safe_nl2sql.validate_sql("DROP TABLE clinical_trials;")

def test_nl2sql_prohibited_delete():
    with pytest.raises(ValueError, match="Security violation"):
        safe_nl2sql.validate_sql("DELETE FROM patients WHERE id = 'PT-001';")

def test_nl2sql_unauthorized_table():
    with pytest.raises(ValueError, match="not allowlisted"):
        safe_nl2sql.validate_sql("SELECT * FROM users;")
