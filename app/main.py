from fastapi import FastAPI
from app.database import engine

app = FastAPI()

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