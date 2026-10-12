from sqlalchemy import Column, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class Interaction(Base, TimestampMixin):
    __tablename__ = "interactions"

    id = Column(String(50), primary_key=True, index=True)
    hcp_id = Column(String(50), ForeignKey("hcps.id"), nullable=False, index=True)
    interaction_date = Column(Date, nullable=False, index=True)
    channel = Column(String(50), nullable=False)  # In-Person Detail, Virtual Call, Email, Webinar
    rep_name = Column(String(100), nullable=False)
    topics_discussed = Column(String(255), nullable=False)
    sentiment = Column(String(20), default="Neutral", nullable=False)  # Positive, Neutral, Hesitant
    notes = Column(Text, nullable=True)

    hcp = relationship("HCP", back_populates="interactions")
