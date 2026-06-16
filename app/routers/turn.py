from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.turn import Turn
from app.models.employee import Employee, SkillLevel
from app.models.customer import Customer
from app.models.service import Service
from app.models.turn_service import TurnService
from app.schemas.turn import TurnCreate, TurnCheckout, TurnUpdate, AutoTurnCreate
from app.utils import get_or_404, find_available_employee
from app.auth import get_current_user, require_roles

router = APIRouter()

@router.post("/turns")
def create_turn(turn: TurnCreate, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    employee = get_or_404(db, Employee, turn.employee_id, detail="Employee not found")
    get_or_404(db, Customer, turn.customer_id, detail="Customer not found")
    
    employee.is_busy = True
    db.add(employee)

    db_turn = Turn(**turn.model_dump())
    db.add(db_turn)
    db.commit()
    db.refresh(db_turn)
    return db_turn

@router.post("/turns/auto")
def auto_create_turn(auto_turn: AutoTurnCreate, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    get_or_404(db, Customer, auto_turn.customer_id, detail="Customer not found")
    services = db.query(Service).filter(Service.id.in_(auto_turn.service_ids)).all()
    hand_services = [s for s in services if s.category.value=="hand"]
    foot_services = [s for s in services if s.category.value=="foot"]

    hand_employee = find_available_employee(db, SkillLevel.HAND)
    foot_employee = find_available_employee(db, SkillLevel.FOOT)

    if not hand_employee and hand_services:
        raise HTTPException(status_code=404, detail="No available employee for hand services")
    
    turns = []
    if hand_employee and hand_services:
        hand_turn = Turn(employee_id=hand_employee.id, customer_id=auto_turn.customer_id)
        hand_employee.is_busy = True
        db.add(hand_turn)
        db.add(hand_employee)
        turns.append(hand_turn)
    
    if not foot_employee and foot_services:
        raise HTTPException(status_code=404, detail="No available employee for foot services")
    
    if foot_employee and foot_services:
        foot_turn = Turn(employee_id=foot_employee.id, customer_id=auto_turn.customer_id)
        foot_employee.is_busy = True
        db.add(foot_turn)
        db.add(foot_employee)
        turns.append(foot_turn)
    db.commit()
    return turns

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
def get_turn_by_employee_id(employee_id: int, date: date, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    get_or_404(db, Employee, employee_id, detail="Employee not found")

    if current_user.role.value == "employee" and current_user.id != employee_id:
        raise HTTPException(status_code=403, detail="Not enough permission")

    return db.query(Turn).filter(Turn.employee_id==employee_id, Turn.date==date).all()

@router.patch("/turns/{turn_id}/checkout")
def checkout_turn(turn_id: int, checkout: TurnCheckout, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    turn = get_or_404(db, Turn, turn_id, detail="Turn not found")

    if turn.is_complete:
        raise HTTPException(status_code=409, detail="Turn already checked out")
    
    employee = get_or_404(db, Employee, turn.employee_id, detail="Employee not found")
    employee.is_busy = False
    db.add(employee)

    customer = get_or_404(db, Customer, turn.customer_id, detail="Customer not found")
    turn_services = db.query(TurnService).filter(TurnService.turn_id==turn_id).all()

    #stamp discount
    new_stamps = sum(1 for ts in turn_services if ts.price_at_time >= 30)
    total_stamps = customer.stamp + new_stamps
    discounts = total_stamps // 10
    customer.stamp = total_stamps % 10
    discount_amount = discounts * 10

    total_service = sum(ts.price_at_time + (ts.extra_charge or 0) for ts in turn_services) - discount_amount

    #birthday discount
    today = date.today()
    if customer.birthday and customer.birthday.month == today.month and customer.birthday.day == today.day:
        total_service = total_service * 0.9

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