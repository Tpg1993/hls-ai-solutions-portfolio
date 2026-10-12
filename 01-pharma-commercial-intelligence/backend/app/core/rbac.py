from enum import Enum
from typing import Dict, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.core.security import decode_access_token

class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    BUSINESS_OWNER = "BUSINESS_OWNER"
    ANALYST = "ANALYST"
    AUDITOR = "AUDITOR"
    STANDARD_USER = "STANDARD_USER"

# Strict Role Hierarchy: higher score inherits lower permissions
ROLE_HIERARCHY: Dict[UserRole, int] = {
    UserRole.SUPER_ADMIN: 100,
    UserRole.ADMIN: 80,
    UserRole.BUSINESS_OWNER: 60,
    UserRole.ANALYST: 40,
    UserRole.AUDITOR: 20,
    UserRole.STANDARD_USER: 10,
}

class TokenPayload(BaseModel):
    sub: str
    role: UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

async def get_current_user_payload(token: Optional[str] = Depends(oauth2_scheme)) -> TokenPayload:
    if not token:
        # In development mode, provide a mock ANALYST user if not passed, or enforce strict auth
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token missing or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    sub: str = payload.get("sub")
    role_str: str = payload.get("role", UserRole.STANDARD_USER)
    
    try:
        role = UserRole(role_str)
    except ValueError:
        role = UserRole.STANDARD_USER
        
    return TokenPayload(sub=sub, role=role)

def require_role(min_role: UserRole):
    """
    Enforces server-side authorization based on role hierarchy.
    Never relies on client-side button hiding.
    """
    async def role_checker(current_user: TokenPayload = Depends(get_current_user_payload)) -> TokenPayload:
        user_level = ROLE_HIERARCHY.get(current_user.role, 0)
        required_level = ROLE_HIERARCHY.get(min_role, 100)
        
        if user_level < required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden: Action requires at least {min_role.value} permission",
            )
        return current_user
    return role_checker
