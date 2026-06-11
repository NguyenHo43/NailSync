from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerPublicResponse, CustomerResponse
from app.utils import get_or_404, check_duplicate
from app.auth import get_current_user, require_roles

router = APIRouter()

@router.post("/customers")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    check_duplicate(db, Customer, Customer.phone, customer.phone, "Phone number already exists")

    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/customers")
def get_customer(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    customers = db.query(Customer).all()

    if current_user.role.value == "employee":
        return [CustomerPublicResponse.model_validate(c) for c in customers]
    
    return [CustomerResponse.model_validate(c) for c in customers]

@router.get("/customers/{customer_id}")
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    customer = get_or_404(db, Customer, customer_id, detail="Customer not found")

    if current_user.role.value == "employee":
        return CustomerPublicResponse.model_validate(customer)
    
    return customer

@router.patch("/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db), current_user: Employee = Depends(require_roles(["owner", "manager"]))):
    db_customer = get_or_404(db, Customer, customer_id, detail="Customer not found")

    update_data = customer.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer
