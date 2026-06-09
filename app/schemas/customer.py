from app.models.enums import GenderType
from app.schemas.base import PhoneModel
from datetime import date
from typing import Optional

class CustomerCreate(PhoneModel):
    name: str
    phone: str
    gender: GenderType
    birthday: Optional[date] = None