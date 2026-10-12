from sqlalchemy import Column, String, JSON
from app.core.database import Base
from app.models.base import TimestampMixin

class AuditEvent(Base, TimestampMixin):
    __tablename__ = "audit_events"

    id = Column(String(50), primary_key=True, index=True)
    user_id = Column(String(50), nullable=False, index=True)
    user_role = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(100), nullable=True)
    details = Column(JSON, nullable=True)
