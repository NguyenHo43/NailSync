from pydantic import BaseModel
from typing import Optional

class TurnServiceCreate(BaseModel):
    turn_id: int
    service_id: int
    extra_charge: Optional[float] = 0