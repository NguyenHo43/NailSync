import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
import os
from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    def overide_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = overide_get_db
    
    from app.auth import hash_password
    from app.models.employee import Employee, SkillLevel
    from app.models.enums import GenderType, Role

    owner = Employee(
        name="Test Owner",
        phone="0000000000",
        gender=GenderType.FEMALE,
        skill_level=SkillLevel.BOTH,
        role=Role.OWNER,
        password=hash_password("testpass"),
        is_employed=True,
        is_active=False
    )
    db.add(owner)
    db.commit()

    test_client = TestClient(app)
    response = test_client.post("/auth/login", json={
        "phone": "0000000000",
        "password": "testpass"
    })
    token = response.json()["access_token"]

    test_client.headers.update({"Authorization": f"Bearer {token}"})

    return test_client

