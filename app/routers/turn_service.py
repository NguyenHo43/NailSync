from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.turn_service import TurnServiceCreate
from app.models.turn_service import TurnService
from app.models.service import Service
from app.database import get_db

router = APIRouter()

@router.post("/turn-services")
def create_turn_service(turn_service_create: TurnServiceCreate, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id==turn_service_create.service_id).first()
    

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
def get_all_turn_services(db: Session = Depends(get_db)):
    return db.query(TurnService).all()

@router.get("/turn-services/turn/{turn_id}")
def get_turn_service_by_turn(turn_id: int, db: Session = Depends(get_db)):
    return db.query(TurnService).filter(TurnService.turn_id==turn_id).all()