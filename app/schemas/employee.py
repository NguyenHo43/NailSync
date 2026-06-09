from app.models.employee import SkillLevel
from app.models.enums import GenderType
from app.schemas.base import PhoneModel

class EmployeeCreate(PhoneModel):
    name: str
    gender: GenderType
    skill_level : SkillLevel
    is_active: bool = True
    turn_order: int = 0
