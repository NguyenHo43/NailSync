import pytest

@pytest.fixture
def sample_employee(client):
    response = client.post("/employees", json={
        "name": "Anna Nguyen",
        "phone": "918-555-0123",
        "gender": "female",
        "skill_level": "both"
    })
    return response.json()

def test_create_employee(client, sample_employee):
    assert sample_employee["name"] == "Anna Nguyen"

def test_employee_not_found(client, sample_employee):
    response = client.get("/employees/999")
    assert response.status_code == 404

def test_update_employee(client, sample_employee):
    employee_id = sample_employee["id"]
    response = client.patch(f"/employees/{employee_id}", json={
        "name": "Anna Tran"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Anna Tran"

def test_delete_employee(client, sample_employee):
    employee_id = sample_employee["id"]
    response = client.delete(f"/employees/{employee_id}")

    assert response.status_code == 200