from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any, List
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

ROLE_HIERARCHY = {
    "SUPER_ADMIN": 100,
    "ADMIN": 80,
    "SAFETY_REVIEWER": 60,
    "ANALYST": 40,
    "AUDITOR": 20,
    "STANDARD_USER": 10
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(min_role: str):
    def role_checker(token: str = Depends(oauth2_scheme)) -> dict:
        payload = decode_token(token)
        user_role = payload.get("role", "STANDARD_USER")
        user_weight = ROLE_HIERARCHY.get(user_role, 0)
        required_weight = ROLE_HIERARCHY.get(min_role, 0)
        if user_weight < required_weight:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires minimum role {min_role}. Current role: {user_role}"
            )
        return payload
    return role_checker
