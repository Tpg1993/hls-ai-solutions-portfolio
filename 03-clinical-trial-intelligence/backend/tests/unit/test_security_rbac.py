import pytest
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.rbac import ROLE_HIERARCHY, UserRole

def test_password_hashing():
    pw = "ClinOpsPass@2026"
    h = get_password_hash(pw)
    assert h != pw
    assert verify_password(pw, h)
    assert not verify_password("Wrong", h)

def test_clinical_rbac_hierarchy():
    assert ROLE_HIERARCHY[UserRole.SUPER_ADMIN] > ROLE_HIERARCHY[UserRole.ADMIN]
    assert ROLE_HIERARCHY[UserRole.ADMIN] > ROLE_HIERARCHY[UserRole.CLINICAL_REVIEWER]
    assert ROLE_HIERARCHY[UserRole.CLINICAL_REVIEWER] > ROLE_HIERARCHY[UserRole.AUDITOR]
    assert ROLE_HIERARCHY[UserRole.AUDITOR] > ROLE_HIERARCHY[UserRole.STANDARD_USER]

def test_token_creation():
    t = create_access_token(subject="user-clin-01", role="CLINICAL_REVIEWER")
    assert isinstance(t, str)
    assert len(t.split(".")) == 3
