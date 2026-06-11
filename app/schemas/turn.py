from pydantic import BaseModel
from typing import Optional

class TurnCreate(BaseModel):
    employee_id: int
    customer_id: int
    total_service: float = 0
    total_tip: float = 0

class TurnCheckout(BaseModel):
    total_tip: float = 0

class TurnUpdate(BaseModel):
    employee_id: Optional[int] = None
    customer_id: Optional[int] = None
    is_complete: Optional[bool] = None