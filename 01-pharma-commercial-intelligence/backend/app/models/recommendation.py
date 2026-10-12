from sqlalchemy import Column, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class Recommendation(Base, TimestampMixin):
    __tablename__ = "recommendations"

    id = Column(String(50), primary_key=True, index=True)
    hcp_id = Column(String(50), ForeignKey("hcps.id"), nullable=False, index=True)
    product_id = Column(String(50), ForeignKey("products.id"), nullable=False, index=True)
    propensity_score = Column(Float, nullable=False)  # Calibrated ML probability [0.0 - 1.0]
    priority_tier = Column(String(20), nullable=False, index=True)  # High, Medium, Low
    recommended_action = Column(String(100), nullable=False)        # e.g., Clinical Detail - Efficacy
    recommended_channel = Column(String(50), nullable=False)       # In-Person Detail, Email, etc.
    top_drivers = Column(JSON, nullable=True)                      # Feature drivers & SHAP weights
    model_version = Column(String(20), default="xgb-v1.0", nullable=False)
    status = Column(String(20), default="PENDING", nullable=False)  # PENDING, ACCEPTED, DISMISSED

    hcp = relationship("HCP", back_populates="recommendations")
