from fastapi import FastAPI
from app.database import engine, Base
from app.models.employee import Employee
from app.models.customer import Customer
from app.routers.employee import router as employee_router
from app.routers.customer import router as customer_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(employee_router)
app.include_router(customer_router)

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