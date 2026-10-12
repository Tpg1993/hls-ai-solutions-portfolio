import pytest
from app.ai.nl2sql import validate_sql_safety

def test_sql_safety_valid():
    valid = "SELECT case_id, suspect_drug, adverse_event FROM safety_cases WHERE severity = 'SERIOUS_HOSPITALIZATION'"
    assert validate_sql_safety(valid) is True

def test_sql_safety_reject_dml_ddl():
    injections = [
        "DROP TABLE safety_cases",
        "DELETE FROM safety_signals WHERE id = 1",
        "INSERT INTO users (username) VALUES ('hacker')",
        "SELECT * FROM users; DROP TABLE safety_cases;",
        "SELECT * FROM secrets_vault"
    ]
    for q in injections:
        assert validate_sql_safety(q) is False
