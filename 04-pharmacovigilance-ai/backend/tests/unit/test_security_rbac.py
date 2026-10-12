import pytest
from fastapi import HTTPException
from app.core.security import verify_password, get_password_hash, create_access_token, decode_token, require_role

def test_password_hashing():
    pw = "SuperSecurePassword123!"
    hashed = get_password_hash(pw)
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_token_creation_and_decoding():
    token = create_access_token({"sub": "safety_doc", "role": "SAFETY_REVIEWER"})
    payload = decode_token(token)
    assert payload["sub"] == "safety_doc"
    assert payload["role"] == "SAFETY_REVIEWER"

def test_role_hierarchy_authorization():
    checker = require_role("SAFETY_REVIEWER")
    # Valid high role token
    valid_token = create_access_token({"sub": "admin_user", "role": "ADMIN"})
    payload = checker(token=valid_token)
    assert payload["role"] == "ADMIN"

    # Lower role unauthorized token
    low_role_token = create_access_token({"sub": "reader", "role": "STANDARD_USER"})
    with pytest.raises(HTTPException) as exc:
        checker(token=low_role_token)
    assert exc.value.status_code == 403
