from sqlalchemy import Integer, Date, Float, Boolean, Column, ForeignKey, func
from app.database import Base

class Turn(Base):
    __tablename__ = "turns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    date = Column(Date, server_default=func.current_date(),nullable=False)
    total_service = Column(Float, default=0, nullable=False)
    total_tip = Column(Float, default=0, nullable=False)
    is_complete = Column(Boolean, default=False)