# tests/test_products.py
# Author: Thanh Trieu
# Description: Contains tests for product-related endpoints.

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_product():
    """
    Test the creation of a new product, including image upload.
    """
    response = client.post(
        "/products/",
        data={
            "name": "Test Product",
            "description": "A product for testing",
            "price": 9.99,
            "stock": 100
        },
        files={"file": ("psyduck.png", open("tests/psyduck.png", "rb"), "image/jpeg")}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
    assert "image_url" in response.json()

def test_upload_product_image():
    """
    Test the upload of an image for a specific product.
    """
    # Create a product to associate with the image
    create_response = client.post(
        "/products/",
        data={
            "name": "Product for Image Upload",
            "description": "A product to upload image",
            "price": 19.99,
            "stock": 50
        }
    )
    product_id = create_response.json()["id"]

    # Upload the image
    image_response = client.post(
        f"/products/{product_id}/upload-image/",
        files={"file": ("psyduck.png", open("tests/psyduck.png", "rb"), "image/jpeg")}
    )

    assert image_response.status_code == 200
    file_url = image_response.json().get("file_url")
    assert file_url is not None
    assert isinstance(file_url, str)

def test_read_product():
    """
    Test retrieving a product by ID, including checking for a pre-signed URL for the image.
    """
    # Create a product
    create_response = client.post(
        "/products/",
        data={
            "name": "Product for Reading",
            "description": "A product to read",
            "price": 29.99,
            "stock": 25
        }
    )
    product_id = create_response.json()["id"]

    # Read the product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Product for Reading"
    assert "image_url" in response.json()
    assert isinstance(response.json()["image_url"], str)

def test_read_products():
    """
    Test retrieving a list of all products with pagination.
    """
    response = client.get("/products/?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_product():
    """
    Test updating an existing product's details.
    """
    # Create a product to update
    create_response = client.post(
        "/products/",
        data={
            "name": "Product to Update",
            "description": "A product to update",
            "price": 19.99,
            "stock": 50
        }
    )
    product_id = create_response.json()["id"]

    # Update the product
    update_response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Updated Product",
            "description": "An updated product",
            "price": 29.99,
            "stock": 40
        }
    )

    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Product"
    assert update_response.json()["price"] == 29.99

def test_delete_product():
    """
    Test deleting a product by ID.
    """
    # Create a product to delete
    create_response = client.post(
        "/products/",
        data={
            "name": "Product to Delete",
            "description": "A product to delete",
            "price": 15.99,
            "stock": 30
        }
    )
    product_id = create_response.json()["id"]

    # Delete the product
    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == product_id

    # Verify the product has been deleted
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404
