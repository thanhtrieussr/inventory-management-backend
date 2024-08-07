# app/crud.py
# Author: Thanh Trieu
# Description: Contains CRUD operations for managing products and orders in the database.

from sqlalchemy.orm import Session
from sqlalchemy import exc
from . import models, schemas

def get_product(db: Session, product_id: int):
    """Retrieve a product by its ID."""
    return db.query(models.Product).filter_by(id=product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve a list of products with pagination."""
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate, image_url: str = None):
    """Create a new product and add it to the database."""
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image_url=image_url
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    """Update an existing product's details."""
    db_product = db.query(models.Product).filter_by(id=product_id).first()
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    """Delete a product by its ID."""
    db_product = db.query(models.Product).filter_by(id=product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

def get_inventory(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve a list of products for inventory management with pagination."""
    inventory = db.query(models.Product).offset(skip).limit(limit).all()
    return [{"product_id": product.id, "stock": product.stock} for product in inventory]

def get_inventory_product(db: Session, product_id: int):
    """Retrieve a product from the inventory by its ID."""
    product = db.query(models.Product).filter_by(id=product_id).first()
    if product:
        return {"product_id": product.id, "stock": product.stock}
    return None

def create_order(db: Session, order: schemas.OrderCreate):
    """Create a new order and handle stock reduction."""
    try:
        db_order = models.Order(total_amount=order.total_amount)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        for item in order.items:
            db_order_item = models.OrderItem(order_id=db_order.id, product_id=item.product_id, quantity=item.quantity)
            db.add(db_order_item)

            product = db.query(models.Product).filter_by(id=item.product_id).first()
            if product:
                if product.stock < item.quantity:
                    raise ValueError(f"Not enough stock for product {product.name}")
                product.stock -= item.quantity
                db.add(product)

        db.commit()
        return db_order
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise e
