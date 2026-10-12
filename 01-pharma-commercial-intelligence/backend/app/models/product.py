from sqlalchemy import Column, String, Float, Date
from app.core.database import Base
from app.models.base import TimestampMixin

class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    therapeutic_area = Column(String(50), nullable=False)  # Oncology, Cardiology
    brand_tier = Column(String(20), default="Primary", nullable=False)
    price_per_unit = Column(Float, default=1500.0, nullable=False)
    competitor_product_name = Column(String(100), nullable=False)
