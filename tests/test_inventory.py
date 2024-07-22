# tests/test_inventory.py
# Author: Thanh Trieu
# Description: Contains tests for inventory-related endpoints.

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_inventory():
    """
    Test retrieving a list of all inventory items with pagination.
    """
    response = client.get("/inventory")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_inventory_product():
    """
    Test retrieving inventory information for a specific product by ID.
    """
    # Create a product
    create_response = client.post(
        "/products/",
        data={
            "name": "Inventory Product",
            "description": "For inventory check",
            "price": 25.99,
            "stock": 15
        }
    )
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    # Check inventory
    inventory_response = client.get(f"/inventory/{product_id}")
    assert inventory_response.status_code == 200
    inventory_data = inventory_response.json()
    assert inventory_data["product_id"] == product_id
    assert inventory_data["stock"] == 15
