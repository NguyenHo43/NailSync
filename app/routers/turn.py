from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.turn import Turn
from app.models.employee import Employee
from app.models.customer import Customer
from app.models.turn_service import TurnService
from app.schemas.turn import TurnCreate, TurnCheckout, TurnUpdate
from app.utils import get_or_404
from app.auth import get_current_user, require_roles

router = APIRouter()

@router.post("/turns")
def create_turn(turn: TurnCreate, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    get_or_404(db, Employee, turn.employee_id, detail="Employee not found")
    get_or_404(db, Customer, turn.customer_id, detail="Customer not found")
    
    db_turn = Turn(**turn.model_dump())
    db.add(db_turn)
    db.commit()
    db.refresh(db_turn)
    return db_turn

@router.get("/turns")
def get_turn(db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    return db.query(Turn).all()

@router.get("/turns/date/{date}")
def get_turn_by_date(date: date, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    return db.query(Turn).filter(Turn.date==date).all()

@router.get("/turns/{turn_id}")
def get_turn_by_id(turn_id: int, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    return get_or_404(db, Turn, turn_id, detail="Turn not found")

@router.get("/turns/employee/{employee_id}/date/{date}")
def get_turn_by_employee_id(employee_id: int, date: date,db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    get_or_404(db, Employee, employee_id, detail="Employee not found")

    if current_user.role.value == "employee" and current_user.id != employee_id:
        raise HTTPException(status_code=403, detail="Not enough permission")

    return db.query(Turn).filter(Turn.employee_id==employee_id, Turn.date==date).all()

@router.patch("/turns/{turn_id}/checkout")
def checkout_turn(turn_id: int, checkout: TurnCheckout, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    turn = get_or_404(db, Turn, turn_id, detail="Turn not found")

    if turn.is_complete:
        raise HTTPException(status_code=409, detail="Turn already checked out")
    
    customer = get_or_404(db, Customer, turn.customer_id, detail="Customer not found")
    turn_services = db.query(TurnService).filter(TurnService.turn_id==turn_id).all()

    new_stamps = sum(1 for ts in turn_services if ts.price_at_time >= 30)
    total_stamps = customer.stamp + new_stamps

    discounts = total_stamps // 10
    customer.stamp = total_stamps % 10

    discount_amount = discounts * 10
    total_service = sum(ts.price_at_time + (ts.extra_charge or 0) for ts in turn_services) - discount_amount

    turn.total_service = total_service
    turn.total_tip = checkout.total_tip
    turn.is_complete = True

    db.add(customer)
    db.commit()
    db.refresh(turn)
    
    return turn

@router.patch("/turns/{turn_id}")
def update_turn(turn_id: int, turn_update: TurnUpdate, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    db_turn = get_or_404(db, Turn, turn_id, detail="Turn not found")

    update_data = turn_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_turn, key, value)

    db.commit()
    db.refresh(db_turn)
    return db_turn