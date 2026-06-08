from fastapi import FastAPI
from app.database import engine, Base
from app.models.employee import Employee
from app.models.customer import Customer
from app.models.service import Service
from app.models.turn_service import TurnService
from app.models.turn import Turn
from app.routers.employee import router as employee_router
from app.routers.customer import router as customer_router
from app.routers.service import router as service_router
from app.routers.turn import router as turn_router
from app.routers.turn_service import router as turn_service_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(employee_router)
app.include_router(customer_router)
app.include_router(service_router)
app.include_router(turn_router)
app.include_router(turn_service_router)

@app.get("/")
def root():
    return {"message": "NailSync API is running"}

@app.get("/health")
def health_check():
    try:
        with engine.connect() as conn:
            return {"status": "Database connected"}
    except Exception as e:
        return {"status": "Connection failed", "error": str(e)}