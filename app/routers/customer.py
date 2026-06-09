from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.utils import get_or_404, check_duplicate

router = APIRouter()

@router.post("/customers")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    check_duplicate(db, Customer, Customer.phone, customer.phone, "Phone number already exists")
    
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/customers")
def get_customer(db: Session = Depends(get_db)):
    return db.query(Customer).all()

@router.get("/customers/{id}")
def get_customer_by_id(id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Customer, id, detail="Customer not found")