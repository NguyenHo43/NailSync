import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.database import Base

class SkillLevel(enum.Enum):
    HAND = "hand"
    FOOT = "foot"
    BOTH = "both"

class GenderType(enum.Enum):
    MALE = "male"
    FEMALE = "female"

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    gender = Column(Enum(GenderType), nullable=False)
    skill_level = Column(Enum(SkillLevel), nullable=False)
    is_active = Column(Boolean, default=True)
    turn_order = Column(Integer, default=0)
    
    
