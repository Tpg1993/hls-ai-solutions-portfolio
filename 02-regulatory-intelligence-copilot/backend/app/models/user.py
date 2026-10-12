from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from app.core.database import Base
from app.models.base import TimestampMixin
from app.core.rbac import UserRole

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.REGULATORY_REVIEWER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
