from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
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
    
@router.get("/employees/{id}")
def get_employee_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(Employee).filter(Employee.id==id).first()