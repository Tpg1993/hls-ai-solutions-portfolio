import pytest
from app.core.rbac import UserRole, ROLE_HIERARCHY

def test_role_hierarchy_ordering():
    assert ROLE_HIERARCHY[UserRole.SUPER_ADMIN] > ROLE_HIERARCHY[UserRole.ADMIN]
    assert ROLE_HIERARCHY[UserRole.ADMIN] > ROLE_HIERARCHY[UserRole.BUSINESS_OWNER]
    assert ROLE_HIERARCHY[UserRole.BUSINESS_OWNER] > ROLE_HIERARCHY[UserRole.ANALYST]
    assert ROLE_HIERARCHY[UserRole.ANALYST] > ROLE_HIERARCHY[UserRole.AUDITOR]
    assert ROLE_HIERARCHY[UserRole.AUDITOR] > ROLE_HIERARCHY[UserRole.STANDARD_USER]

def test_analyst_cannot_access_admin_level():
    analyst_score = ROLE_HIERARCHY[UserRole.ANALYST]
    admin_score = ROLE_HIERARCHY[UserRole.ADMIN]
    assert analyst_score < admin_score
