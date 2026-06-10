from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate
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

@router.get("/services/{service_id}")
def get_service_by_id(service_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Service, service_id, detail="Service not found")

@router.patch("/services/{service_id}")
def update_service(service_id: int, service: ServiceUpdate,db: Session = Depends(get_db)):
    db_service = get_or_404(db, Service, service_id, detail="Service not found")

    update_data = service.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)
    
    db.commit()
    db.refresh(db_service)
    return db_service

@router.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = get_or_404(db, Service, service_id, detail="Service not found")

    db_service.is_available = False
    db.commit()
    return {"message": "Service deleted succesfully"}