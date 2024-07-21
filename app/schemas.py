# schemas.py
from typing import List
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    image_url: str

    class Config:
        orm_mode = True


class Inventory(BaseModel):
    product_id: int
    stock: int

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    total_amount: float


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    items: List[OrderItem]

    class Config:
        orm_mode = True
