def test_create_service(client):
    response = client.post("/services", json={
        "name": "Deluxe Pedicure",
        "category": "foot",
        "base_price": 49
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Deluxe Pedicure"

def test_service_not_found(client):
    response = client.get("/services/959")
    assert response.status_code == 404