from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.turn import Turn
from app.models.employee import Employee
from app.models.customer import Customer
from app.schemas.turn import TurnCreate
from app.utils import get_or_404
router = APIRouter()

@router.post("/turns")
def create_turn(turn: TurnCreate, db: Session = Depends(get_db)):
    get_or_404(db, Employee, turn.employee_id, detail="Employee not found")
    get_or_404(db, Customer, turn.customer_id, detail="Customer not found")
    
    db_turn = Turn(**turn.model_dump())
    db.add(db_turn)
    db.commit()
    db.refresh(db_turn)
    return db_turn

@router.get("/turns")
def get_turn(db: Session = Depends(get_db)):
    return db.query(Turn).all()

@router.get("/turns/date/{date}")
def get_turn_by_date(date: date, db: Session = Depends(get_db)):
    return db.query(Turn).filter(Turn.date==date).all()

@router.get("/turns/employee/{employee_id}/date/{date}")
def get_turn_by_employee_id(employee_id: int, date: date,db: Session = Depends(get_db)):
    get_or_404(db, Employee, employee_id, detail="Employee not found")
    return db.query(Turn).filter(Turn.employee_id==employee_id, Turn.date==date).all()