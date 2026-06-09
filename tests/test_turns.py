def test_create_turn(client):
    emp = client.post("/employees", json={
        "name": "Jennifer Tran",
        "phone": "918-345-0123",
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

    response = client.post("/turns", json={
       "employee_id": employee_id,
       "customer_id": customer_id
    })
    
    assert response.status_code == 200
    assert response.json()["employee_id"] == employee_id
    
def test_turn_not_found(client):
    response = client.get("/turns/999")

    assert response.status_code == 404
