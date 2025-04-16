from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, validator

# ---------- CREACIÓN ----------

class InvoiceItemCreate(BaseModel):
    description: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., ge=0)

    @validator("description")
    def no_blank_description(cls, v):
        if not v.strip():
            raise ValueError("La descripción no puede estar vacía o en blanco.")
        return v

    class Config:
        from_attributes = True


class InvoiceCreate(BaseModel):
    provider: str = Field(..., min_length=1)
    total: float = Field(..., ge=0)
    date: str  # Podrías cambiar a `date` si querés validación automática

    @validator("provider")
    def no_blank_provider(cls, v):
        if not v.strip():
            raise ValueError("El proveedor no puede estar vacío.")
        return v

    class Config:
        from_attributes = True


class InvoiceWithItems(InvoiceCreate):
    items: list[InvoiceItemCreate]


# ---------- SALIDA (RESPUESTA) ----------

class InvoiceItemOut(BaseModel):
    id: int
    description: str
    quantity: int
    price: float

    class Config:
        from_attributes = True


class InvoiceOut(BaseModel):
    id: int
    provider: str
    total: float
    date: date
    items: list[InvoiceItemOut] = []

    class Config:
        from_attributes = True


# ---------- ACTUALIZACIÓN ----------

class InvoiceUpdate(BaseModel):
    provider: Optional[str] = None
    total: Optional[float] = None
    date: Optional[str] = None

    @validator("provider")
    def no_blank_provider(cls, v):
        if v is not None and not v.strip():
            raise ValueError("El proveedor no puede estar vacío.")
        return v

    class Config:
        from_attributes = True


class InvoiceItemUpdate(BaseModel):
    description: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., ge=0)

    @validator("description")
    def no_blank_description(cls, v):
        if not v.strip():
            raise ValueError("La descripción no puede estar vacía o en blanco.")
        return v

    class Config:
        from_attributes = True


class InvoiceItemsUpdate(BaseModel):
    items: list[InvoiceItemUpdate]

    class Config:
        from_attributes = True
