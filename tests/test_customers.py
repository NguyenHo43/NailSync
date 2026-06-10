import pytest

def test_create_customer(client):
    response = client.post("/customers", json={
        "name": "Sarah Smith",
        "phone": "918-123-4567",
        "gender": "female",
        "birthday": "1995-06-02"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Sarah Smith"

def test_customer_not_found(client):
    response = client.get("/customers/567")
    assert response.status_code == 404