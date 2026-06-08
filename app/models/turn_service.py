from app.database import Base
from sqlalchemy import Column, Integer, Float, ForeignKey

class TurnService(Base):
    __tablename__ = "turn_service"

    id = Column(Integer, primary_key=True, autoincrement=True)
    turn_id = Column(Integer, ForeignKey("turns.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    price_at_time = Column(Float, nullable=False)
    extra_charge = Column(Float, nullable=True)