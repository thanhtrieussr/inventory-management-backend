from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order():
    # Create a product
    product_response = client.post(
        "/products/",
        data={
            "name": "Order Product",
            "description": "For ordering",
            "price": 30.99,
            "stock": 20
        }
    )
    product_id = product_response.json()["id"]

    # Create an order
    order_response = client.post(
        "/orders/",
        json={
            "total_amount": 30.99,
            "items": [
                {"product_id": product_id, "quantity": 1}
            ]
        }
    )
    assert order_response.status_code == 200
    order_data = order_response.json()
    assert order_data["total_amount"] == 30.99
    assert len(order_data["items"]) == 1
    assert order_data["items"][0]["product_id"] == product_id
