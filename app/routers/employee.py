from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.turn import Turn
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.utils import get_or_404, check_duplicate
from app.auth import hash_password, get_current_user,  require_roles
from typing import List


router = APIRouter()

@router.post("/employees")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    check_duplicate(db, Employee, Employee.phone, employee.phone, "Phone number already exists")
    
    employee_data = employee.model_dump()
    employee_data["password"] = hash_password(employee_data["password"])

    db_employee = Employee(**employee_data)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.post("/employees/{employee_id}/checkin")
def employee_check_in(employee_id: int, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    employee = get_or_404(db, Employee, employee_id, detail="Employee not found")
    current_active = db.query(Employee).filter(Employee.is_active==True).count()
    employee.is_active = True
    employee.turn_order = current_active + 1
    db.add(employee)
    db.commit()
    return employee

@router.post("/employees/{employee_id}/checkout")
def employee_check_out(employee_id: int, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    employee = get_or_404(db, Employee, employee_id, detail="Employee not found")
    employee.is_active = False
    employee.is_busy = False
    employee.turn_order = 0
    db.add(employee)
    db.commit()
    return employee

@router.get("/employees", response_model=List[EmployeeResponse])
def get_employee(db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    return db.query(Employee).all()
    
@router.get("/employees/{employee_id}")
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    if current_user.role.value == "employee" and current_user.id != employee_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return get_or_404(db, Employee, employee_id, detail="Employee not found")

@router.get("/employees/{employee_id}/salary")
def get_salary(employee_id: int, month: int, year: int,db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    get_or_404(db, Employee, employee_id, detail="Employee not found")


    if current_user.role.value == "employee" and current_user.id != employee_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    turns = db.query(Turn).filter(Turn.employee_id == employee_id,
                                  func.extract('month', Turn.date)==month,
                                  func.extract('year', Turn.date)==year,
                                  Turn.is_complete==True).all()
    
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

@router.patch("/employees/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    db_employee = get_or_404(db, Employee, employee_id, detail="Employee not found")

    update_data = employee.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner"]))):
    db_employee = get_or_404(db, Employee, employee_id, detail="Employee not found")

    db_employee.is_employed = False
    db.commit()
    return {"message": "Employee deleted successfully"}