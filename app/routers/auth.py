from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.schemas.auth import LoginRequest
from app.auth import verify_password, create_access_token

router = APIRouter()
@router.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.phone==request.phone).first()
    if not employee:
        raise HTTPException(status_code=401, detail="Invalid phone or password")
    
    if not verify_password(request.password, employee.password):
        raise HTTPException(status_code=401, detail="Invalid phone or password")
    
    token = create_access_token({"sub": str(employee.id), "role": employee.role.value})

    return{"access_token": token, "token_type": "bearer"}