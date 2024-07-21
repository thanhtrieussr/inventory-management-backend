# routers/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, models, database

router = APIRouter()


@router.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    db_order = crud.create_order(db=db, order=order)
    if not db_order:
        raise HTTPException(status_code=400, detail="Order could not be created")
    return db_order
