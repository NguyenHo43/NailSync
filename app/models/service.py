from sqlalchemy import Column, Integer, String, Float, Enum, Boolean
from app.database import Base
import enum

class ServiceCategory(enum.Enum):
    HAND = "hand"
    FOOT = "foot"
    ADDON = "addon"

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    category = Column(Enum(ServiceCategory), nullable=False)
    base_price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)