from pydantic import BaseModel
from app.models.service import ServiceCategory

class ServiceCreate(BaseModel):
    name: str
    category: ServiceCategory
    base_price: float