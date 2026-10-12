from sqlalchemy import Column, String, Float, Integer
from app.core.database import Base
from app.models.base import TimestampMixin

class Territory(Base, TimestampMixin):
    __tablename__ = "territories"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    region = Column(String(50), nullable=False)  # North, South, East, West
    quota = Column(Float, default=1000000.0, nullable=False)
    assigned_rep_name = Column(String(100), nullable=False)
    assigned_rep_email = Column(String(100), nullable=False)
    target_specialty = Column(String(50), default="Oncology", nullable=False)
