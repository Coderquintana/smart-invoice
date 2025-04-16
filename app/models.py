from sqlalchemy import Column, Integer, String, Float
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String)
    total = Column(Float)
    date = Column(String)

    items = relationship("InvoiceItem",back_populates="invoice",cascade="all, delete", lazy="joined")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    description = Column(String)
    quantity = Column(Integer)
    price = Column(Float)

    invoice = relationship("Invoice", back_populates="items")


