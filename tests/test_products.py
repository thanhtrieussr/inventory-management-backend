from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_product():
    response = client.post("/api/v1/products/",
                           json={"name": "Test Product", "description": "A product for testing", "price": 9.99,
                                 "stock_level": 100, "image_url": "http://example.com/image.jpg"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
