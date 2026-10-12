from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class HCP(Base, TimestampMixin):
    __tablename__ = "hcps"

    id = Column(String(50), primary_key=True, index=True)
    npi_synthetic = Column(String(10), unique=True, index=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    specialty = Column(String(50), index=True, nullable=False)  # Oncology, Cardiology, etc.
    hospital_affiliation = Column(String(150), nullable=False)
    address = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(10), index=True, nullable=False)
    zip_code = Column(String(10), nullable=False)
    territory_id = Column(String(50), ForeignKey("territories.id"), nullable=False, index=True)
    decile = Column(Integer, default=5, nullable=False)  # 1 to 10 volume tier
    digital_affinity = Column(String(20), default="Medium", nullable=False)  # High, Medium, Low
    adoption_stage = Column(String(30), default="Advocate", nullable=False)  # Trialist, Skeptic, Advocate
    
    # Relationships
    prescriptions = relationship("Prescription", back_populates="hcp", cascade="all, delete-orphan")
    interactions = relationship("Interaction", back_populates="hcp", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="hcp", cascade="all, delete-orphan")
