from pydantic import BaseModel
from app.models.enums import GenderType
from datetime import date
from typing import Optional

class CustomerCreate(BaseModel):
    name: str
    phone: str
    gender: GenderType
    birthday: Optional[date] = None