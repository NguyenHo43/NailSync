import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.database import Base
from app.models.enums import GenderType, Role

class SkillLevel(enum.Enum):
    HAND = "hand"
    FOOT = "foot"
    BOTH = "both"

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(Enum(Role), default=Role.EMPLOYEE)
    password= Column(String, nullable=False)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    gender = Column(Enum(GenderType), nullable=False)
    skill_level = Column(Enum(SkillLevel), nullable=False)
    is_employed = Column(Boolean, default=True)
    is_active = Column(Boolean, default=False)
    turn_order = Column(Integer, default=0)
    is_busy = Column(Boolean, default=False)
    
    
