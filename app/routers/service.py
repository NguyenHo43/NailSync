from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.service import Service
from app.schemas.service import ServiceCreate
from app.utils import get_or_404

router = APIRouter()

@router.post("/services")
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.get("/services")
def get_service(db: Session = Depends(get_db)):
    return db.query(Service).all()

@router.get("/services/{id}")
def get_service_by_id(id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Service, id, detail="Service not found")