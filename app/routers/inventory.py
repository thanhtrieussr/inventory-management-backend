# app/routers/inventory.py
# Author: Thanh Trieu
# Description: Provides endpoints for retrieving inventory information.

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter()

@router.get("/inventory", response_model=List[schemas.Inventory])
def read_inventory(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    """
    Get a list of all inventory items with pagination.
    """
    inventory = crud.get_inventory(db, skip=skip, limit=limit)
    return inventory

@router.get("/inventory/{product_id}", response_model=schemas.Inventory)
def read_inventory_product(product_id: int, db: Session = Depends(database.get_db)):
    """
    Get inventory information for a specific product by ID.
    """
    inventory = crud.get_inventory_product(db, product_id=product_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return inventory
