from pydantic import BaseModel
from typing import Optional
import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    role: str = "analyst"

class ProductCreate(BaseModel):
    name: str
    sku: Optional[str]
    category: Optional[str]
    supplier_id: Optional[int]

class InventoryCreate(BaseModel):
    product_id: int
    location_id: str
    quantity: int

class InventoryOut(BaseModel):
    id: int
    product_id: int
    location_id: str
    quantity: int
    last_updated: datetime.datetime
    class Config:
        orm_mode = True
