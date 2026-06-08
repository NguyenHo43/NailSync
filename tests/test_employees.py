
def test_create_employee(client):
    response = client.post("/employees", json={
        "name": "Anna Nguyen",
        "phone": "918-555-0123",
        "gender": "female",
        "skill_level": "both"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Anna Nguyen"

def test_employee_not_found(client):
    response = client.get("/employees/999")
    assert response.status_code == 404