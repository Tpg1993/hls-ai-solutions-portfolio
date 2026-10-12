import pytest
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.rbac import ROLE_HIERARCHY, UserRole

def test_password_hashing():
    pw = "SecretRegPass@2026"
    h = get_password_hash(pw)
    assert h != pw
    assert verify_password(pw, h)
    assert not verify_password("WrongPassword", h)

def test_rbac_hierarchy():
    assert ROLE_HIERARCHY[UserRole.SUPER_ADMIN] > ROLE_HIERARCHY[UserRole.ADMIN]
    assert ROLE_HIERARCHY[UserRole.ADMIN] > ROLE_HIERARCHY[UserRole.REGULATORY_REVIEWER]
    assert ROLE_HIERARCHY[UserRole.REGULATORY_REVIEWER] > ROLE_HIERARCHY[UserRole.AUDITOR]
    assert ROLE_HIERARCHY[UserRole.AUDITOR] > ROLE_HIERARCHY[UserRole.STANDARD_USER]

def test_jwt_token_generation():
    token = create_access_token(subject="user-123", role="REGULATORY_REVIEWER")
    assert isinstance(token, str)
    assert len(token.split(".")) == 3
