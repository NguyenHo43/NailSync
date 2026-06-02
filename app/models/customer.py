from sqlalchemy import Column, Integer, String, Enum, Date
from app.database import Base
from app.models.enums import GenderType

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    gender = Column(Enum(GenderType), nullable=False)
    stamp = Column(Integer, default=0)
    birthday = Column(Date, nullable=True)