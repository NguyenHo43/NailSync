import pytest

@pytest.fixture
def sample_service(client):
    response = client.post("/services", json={
        "name": "Deluxe Pedicure",
        "category": "foot",
        "base_price": 49
    })
    return response.json()

def test_create_service(client, sample_service):
    assert sample_service["name"] == "Deluxe Pedicure"

def test_service_not_found(client):
    response = client.get("/services/999")

    assert response.status_code == 404

def test_update_service(client, sample_service):
    service_id = sample_service["id"]
    response = client.patch(f"/services/{service_id}", json={
        "name": "Vip Pedicure"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Vip Pedicure"

def test_delete_service(client, sample_service):
    service_id = sample_service["id"]
    response = client.delete(f"/services/{service_id}")

    assert response.status_code == 200
