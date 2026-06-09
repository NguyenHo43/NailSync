from pydantic import BaseModel

class TurnCreate(BaseModel):
    employee_id: int
    customer_id: int
    total_service: float = 0
    total_tip: float = 0

class TurnCheckout(BaseModel):
    total_tip: float = 0