from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class Prescription(Base, TimestampMixin):
    __tablename__ = "prescriptions"

    id = Column(String(50), primary_key=True, index=True)
    hcp_id = Column(String(50), ForeignKey("hcps.id"), nullable=False, index=True)
    product_id = Column(String(50), ForeignKey("products.id"), nullable=False, index=True)
    month_year = Column(String(7), nullable=False, index=True)  # YYYY-MM
    trx_count = Column(Integer, default=0, nullable=False)      # Total Prescriptions
    nrx_count = Column(Integer, default=0, nullable=False)      # New Prescriptions
    competitor_trx_count = Column(Integer, default=0, nullable=False)

    hcp = relationship("HCP", back_populates="prescriptions")
