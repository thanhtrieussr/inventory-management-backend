import pytest
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db

def test_read_empty_inventory(client):
    response = client.get("/inventory/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_and_read_inventory(client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 10.0,
        "stock": 100
    }
    product_response = client.post("/products/", data=product_data)
    assert product_response.status_code == 200

    response = client.get("/inventory/")
    assert response.status_code == 200
    inventory = response.json()
    assert len(inventory) == 1
    assert inventory[0]["name"] == "Test Product"
    assert inventory[0]["stock"] == 100

def test_read_inventory_product(client):
    product_data = {
        "name": "Test Product 2",
        "description": "Test Description 2",
        "price": 20.0,
        "stock": 50
    }
    product_response = client.post("/products/", data=product_data)
    assert product_response.status_code == 200
    product = product_response.json()

    response = client.get(f"/inventory/{product['id']}")
    assert response.status_code == 200
    inventory = response.json()
    assert inventory["product_id"] == product["id"]
    assert inventory["stock"] == 50
