from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class TrialSite(Base, TimestampMixin):
    __tablename__ = "trial_sites"

    id = Column(String(50), primary_key=True, index=True)
    site_number = Column(String(50), unique=True, index=True, nullable=False)
    site_name = Column(String(100), nullable=False)
    institution = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    pi_name = Column(String(100), nullable=False) # Principal Investigator

    metric = relationship("SiteMetric", back_populates="site", uselist=False, cascade="all, delete-orphan")

class SiteMetric(Base, TimestampMixin):
    __tablename__ = "site_metrics"

    id = Column(String(50), primary_key=True, index=True)
    site_id = Column(String(50), ForeignKey("trial_sites.id"), nullable=False, unique=True)
    target_patients = Column(Integer, default=20, nullable=False)
    actual_enrolled = Column(Integer, default=0, nullable=False)
    screening_velocity_per_month = Column(Float, default=1.0, nullable=False)
    screen_failure_rate = Column(Float, default=0.25, nullable=False) # e.g. 0.40 = 40%
    activation_delay_days = Column(Integer, default=30, nullable=False)
    dropout_rate = Column(Float, default=0.08, nullable=False)
    predicted_risk = Column(String(20), default="Medium", nullable=False) # High, Medium, Low
    risk_score = Column(Float, default=0.5, nullable=False) # 0.0 to 1.0

    site = relationship("TrialSite", back_populates="metric")
