import pytest

@pytest.fixture
def sample_customer(client):
    response = client.post("/customers", json={
        "name": "Sarah Smith",
        "phone": "918-123-4567",
        "gender": "female",
        "birthday": "1995-06-02"
    })
    return response.json()

def test_create_customer(client, sample_customer):
    assert sample_customer["name"] == "Sarah Smith"

def test_customer_not_found(client):
    response = client.get("/customers/999")
    assert response.status_code == 404

def test_update_customer(client, sample_customer):
    customer_id = sample_customer["id"]
    response = client.patch(f"/customers/{customer_id}", json={
        "name": "Thu Smith"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Thu Smith"
    