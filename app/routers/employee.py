from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.turn import Turn
from app.schemas.employee import EmployeeCreate


router = APIRouter()

@router.post("/employees")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/employees")
def get_employee(db: Session = Depends(get_db)):
    return db.query(Employee).all()
    
@router.get("/employees/{employee_id}")
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    return db.query(Employee).filter(Employee.id==id).first()

@router.get("/employees/{employees_id}/salary")
def get_salary(employee_id: int, month: int, year: int,db: Session = Depends(get_db)):
    turns = db.query(Turn).filter(Turn.employee_id == employee_id,
                                  func.extract('month', Turn.date)==month,
                                  func.extract('year', Turn.date)==year).all()
    
    total_service = sum(turn.total_service for turn in turns)
    total_tip = sum(turn.total_tip for turn in turns)

    return {
        "employee_id": employee_id,
        "month": month,
        "year": year,
        "total_service": total_service,
        "total_tip": total_tip,
        "total": total_service + total_tip
    }