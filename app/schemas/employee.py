from pydantic import BaseModel
from app.models.employee import SkillLevel
from app.models.enums import GenderType

class EmployeeCreate(BaseModel):
    name: str
    phone: str
    gender: GenderType
    skill_level : SkillLevel
    is_active: bool = True
    turn_order: int = 0
