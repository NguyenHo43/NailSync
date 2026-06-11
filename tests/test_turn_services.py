def test_create_turn_service(client):
    emp = client.post("/employees", json={
        "name": "Bina Nguyen",
        "phone": "918-335-4523",
        "gender": "female",
        "skill_level": "both",
        "password": "test123"
    })
    employee_id = emp.json()["id"]

    cus = client.post("/customers", json={
        "name": "Kim Le",
        "phone": "918-423-7847",
        "gender": "female",
        "birthday": "1995-06-02"
    })
    customer_id = cus.json()["id"]

    ser = client.post("/services", json={
        "name": "Fullset Dip",
        "category": "hand",
        "base_price": 50
    })
    service_id = ser.json()["id"]

    turn = client.post("/turns", json={
       "employee_id": employee_id,
       "customer_id": customer_id
    })
    turn_id = turn.json()["id"]

    response = client.post("/turn-services", json={
       "turn_id": turn_id,
       "service_id": service_id,
       "extra_charge": 10
    })

    assert response.status_code == 200
    assert response.json()["extra_charge"] == 10