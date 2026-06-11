from app.models.enums import GenderType
from app.schemas.base import PhoneModel, BaseModel
from datetime import date
from typing import Optional

class CustomerCreate(PhoneModel):
    name: str
    phone: str
    gender: GenderType
    birthday: Optional[date] = None

class CustomerUpdate(PhoneModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[GenderType] = None
    birthday: Optional[date] = None

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    gender: GenderType
    stamp: int
    birthday: Optional[date] = None

    class Config:
        from_attributes = True

class CustomerPublicResponse(BaseModel):
    id: int
    name: str
    gender: GenderType
    stamp: int
    birthday: Optional[date] = None

    class Config:
        from_attributes = True
