from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
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

@router.get("/customers/{customer_id}")
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Customer, customer_id, detail="Customer not found")

@router.patch("/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = get_or_404(db, Customer, customer_id, detail="Customer not found")

    update_data = customer.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer
