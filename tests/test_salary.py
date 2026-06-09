def test_employee_salary(client):
    emp = client.post("/employees", json={
        "name": "Jasmine Nguyen",
        "phone": "918-335-4523",
        "gender": "female",
        "skill_level": "both"
    })
    employee_id = emp.json()["id"]

    cus = client.post("/customers", json={
        "name": "Andrew Smith",
        "phone": "918-433-4547",
        "gender": "male",
        "birthday": "1995-06-02"
    })
    customer_id = cus.json()["id"]

    ser = client.post("/services", json={
        "name": "Ultimate Perdicure",
        "category": "foot",
        "base_price": 90
    })
    service_id = ser.json()["id"]

    turn = client.post("/turns", json={
       "employee_id": employee_id,
       "customer_id": customer_id
    })
    turn_id = turn.json()["id"]

    turn_ser = client.post("/turn-services", json={
       "turn_id": turn_id,
       "service_id": service_id,
       "extra_charge": 5
    })
    turn_ser_id = turn_ser.json()["id"]

    ck = client.patch(f"/turns/{turn_id}/checkout", json={
        "total_tip": 10
    })

    response = client.get(f"/employees/{employee_id}/salary", params={
        "month": 6,
        "year": 2026
        })
    
    assert response.status_code == 200
    assert response.json()["total_service"] == 95
    assert response.json()["total_tip"] == 10


