import pytest

def test_auto_create_hand_turn(client):
    emp = client.post("/employees", json={
        "name": "Hand Tech",
        "phone": "918-111-1111",
        "gender": "female",
        "skill_level": "hand",
        "password": "test123",
        "is_active": True
    })
    
    cus = client.post("/customers", json={
        "name": "Test Customer",
        "phone": "918-222-2222",
        "gender": "female"
    })
    customer_id = cus.json()["id"]
    
    ser = client.post("/services", json={
        "name": "Manicure",
        "category": "hand",
        "base_price": 30
    })
    service_id = ser.json()["id"]
    
    response = client.post("/turns/auto", json={
        "customer_id": customer_id,
        "service_ids": [service_id],
        "same_time": False
    })
    assert response.status_code == 200
    assert len(response.json()) == 1
