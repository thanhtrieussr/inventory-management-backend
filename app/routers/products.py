# app/routers/products.py
# Author: Thanh Trieu
# Description: Provides CRUD operations for products, including image upload and URL generation.

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas, database
from ..utils.s3_utils import upload_file_to_s3, generate_presigned_url
import uuid

router = APIRouter()

def get_db():
    """Dependency to get the database session."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/products/", response_model=schemas.Product)
async def create_product(
        name: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        stock: int = Form(...),
        file: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db)
):
    """
    Create a new product. Optionally upload an image to S3.
    """
    product_data = {
        "name": name,
        "description": description,
        "price": price,
        "stock": stock
    }
    product_schema = schemas.ProductCreate(**product_data)

    file_url = None
    if file:
        filename = f"products/{str(uuid.uuid4())}_{file.filename}"
        file_url = upload_file_to_s3(file, filename)

    return crud.create_product(db=db, product=product_schema, image_url=file_url)

@router.post("/products/{product_id}/upload-image/")
async def upload_product_image(
        product_id: int,
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    """
    Upload an image for a specific product.
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    filename = f"products/{product_id}/{file.filename}"
    try:
        file_url = upload_file_to_s3(file, filename)
        db_product.image_url = file_url
        db.commit()
        db.refresh(db_product)
        return {"file_url": file_url}
    except HTTPException as e:
        raise e

@router.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific product by ID, including a pre-signed URL for the image.
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if db_product.image_url:
        filename = db_product.image_url.split('/')[-1]
        db_product.image_url = generate_presigned_url(filename)

    return db_product

@router.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get a list of all products with pagination.
    """
    products = crud.get_products(db, skip=skip, limit=limit)
    for product in products:
        if product.image_url:
            filename = product.image_url.split('/')[-1]
            product.image_url = generate_presigned_url(filename)
    return products

@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """
    Update an existing product by ID.
    """
    return crud.update_product(db, product_id=product_id, product=product)

@router.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product by ID.
    """
    return crud.delete_product(db, product_id=product_id)
