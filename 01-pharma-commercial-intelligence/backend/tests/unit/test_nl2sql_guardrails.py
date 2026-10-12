import pytest
from app.ai.nl2sql import safe_nl2sql

def test_valid_select_queries():
    valid_query = "SELECT id, first_name, last_name, specialty FROM hcps WHERE decile >= 8 LIMIT 20;"
    is_valid, msg = safe_nl2sql.validate_sql(valid_query)
    assert is_valid is True
    assert msg == "Valid"

def test_disallowed_drop_query():
    drop_query = "DROP TABLE hcps;"
    is_valid, msg = safe_nl2sql.validate_sql(drop_query)
    assert is_valid is False
    assert "Forbidden SQL keyword" in msg or "Only SELECT" in msg

def test_disallowed_update_query():
    update_query = "UPDATE hcps SET decile = 10 WHERE id = 'HCP-001';"
    is_valid, msg = safe_nl2sql.validate_sql(update_query)
    assert is_valid is False

def test_disallowed_delete_query():
    delete_query = "DELETE FROM prescriptions WHERE trx_count = 0;"
    is_valid, msg = safe_nl2sql.validate_sql(delete_query)
    assert is_valid is False

def test_disallowed_table_reference():
    unauthorized_query = "SELECT * FROM secret_system_passwords;"
    is_valid, msg = safe_nl2sql.validate_sql(unauthorized_query)
    assert is_valid is False
