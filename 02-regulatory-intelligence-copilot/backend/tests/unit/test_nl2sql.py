import pytest
from app.ai.nl2sql import safe_nl2sql

def test_safe_sql_validation_allowed():
    valid_query = "SELECT title, authority, publication_date FROM guidance_documents WHERE authority = 'FDA';"
    safe_nl2sql.validate_sql(valid_query)

def test_prohibited_sql_drop():
    with pytest.raises(ValueError, match="Security violation"):
        safe_nl2sql.validate_sql("DROP TABLE guidance_documents;")

def test_prohibited_sql_insert():
    with pytest.raises(ValueError, match="Security violation"):
        safe_nl2sql.validate_sql("INSERT INTO guidance_documents (id, title) VALUES ('x', 'y');")

def test_non_allowlisted_table():
    with pytest.raises(ValueError, match="not allowlisted"):
        safe_nl2sql.validate_sql("SELECT * FROM users;")
