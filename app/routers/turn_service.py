from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.turn_service import TurnServiceCreate
from app.models.turn_service import TurnService
from app.models.employee import Employee
from app.models.service import Service
from app.models.turn import Turn
from app.database import get_db
from app.utils import get_or_404
from app.auth import get_current_user, require_roles

router = APIRouter()

@router.post("/turn-services")
def create_turn_service(turn_service_create: TurnServiceCreate, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    get_or_404(db, Turn, turn_service_create.turn_id, detail="Turn not found")
    service = get_or_404(db, Service, turn_service_create.service_id, detail="Service not found")
    
    db_tsc = TurnService(
        turn_id=turn_service_create.turn_id,
        service_id=turn_service_create.service_id,
        price_at_time=service.base_price,
        extra_charge=turn_service_create.extra_charge
    )
    db.add(db_tsc)
    db.commit()
    db.refresh(db_tsc)
    return db_tsc

@router.get("/turn-services")
def get_all_turn_services(db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    return db.query(TurnService).all()

@router.get("/turn-services/turn/{turn_id}")
def get_turn_service_by_turn(turn_id: int, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    turn = get_or_404(db, Turn, turn_id, detail="Turn not found")
    if current_user.role.value == "employee" and turn.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db.query(TurnService).filter(TurnService.turn_id==turn_id).all()

@router.delete("/turn-services/{turn_service_id}")
def delete_turn_service(turn_service_id: int, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    db_turn_service = get_or_404(db, TurnService, turn_service_id, detail="Turn service not found")

    db.delete(db_turn_service)
    db.commit()
    return {"message": "Turn service deleted succesfully"}
    