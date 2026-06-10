from app.models.employee import SkillLevel
from app.models.enums import GenderType
from app.schemas.base import PhoneModel
from typing import Optional

class EmployeeCreate(PhoneModel):
    name: str
    gender: GenderType
    skill_level : SkillLevel
    is_employed: bool = True
    is_active: bool = False
    turn_order: int = 0

class EmployeeUpdate(PhoneModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[GenderType] = None
    skill_level: Optional[SkillLevel] = None
    is_employed: Optional[bool] = None
    is_active: Optional[bool] = None
    turn_order: Optional[int] = None