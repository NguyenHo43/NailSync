from pydantic import BaseModel
from app.models.service import ServiceCategory
from typing import Optional

class ServiceCreate(BaseModel):
    name: str
    category: ServiceCategory
    base_price: float

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[ServiceCategory] = None
    base_price: Optional[float] = None
    is_available: Optional[bool] = None