from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.turn import Turn
from app.schemas.employee import EmployeeCreate
from app.utils import get_or_404, check_duplicate


router = APIRouter()

@router.post("/employees")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    check_duplicate(db, Employee, Employee.phone, employee.phone, "Phone number already exists")
    
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
    return get_or_404(db, Employee, employee_id, detail="Employee not found")

@router.get("/employees/{employee_id}/salary")
def get_salary(employee_id: int, month: int, year: int,db: Session = Depends(get_db)):
    get_or_404(db, Employee, employee_id, detail="Employee not found")
    
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