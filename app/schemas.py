from pydantic import BaseModel
from typing import List

class InvoiceCreate(BaseModel):
    provider: str
    total: float
    date: str

class InvoiceItemCreate(BaseModel):
    description: str
    quantity: int
    price: float

class InvoiceWithItems(BaseModel):
    provider: str
    total: float
    date: str
    items: List[InvoiceItemCreate]
