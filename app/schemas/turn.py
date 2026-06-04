from pydantic import BaseModel

class TurnCreate(BaseModel):
    employee_id: int
    customer_id: int
    total_service: float
    total_tip: float