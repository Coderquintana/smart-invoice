from sqlalchemy.orm import Session
from app.models import Invoice, InvoiceItem
from app.schemas import InvoiceUpdate, InvoiceItemUpdate
from typing import Optional

def save_invoice_with_items(db: Session, invoice_data: dict, items_data: list) -> Invoice:
    invoice = Invoice(
        provider=invoice_data["provider"],
        total=invoice_data["total"],
        date=invoice_data["date"]
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    for item in items_data:
        invoice_item = InvoiceItem(
            invoice_id=invoice.id,
            description=item["description"],
            quantity=item["quantity"],
            price=item["price"]
        )
        db.add(invoice_item)

    db.commit()
    db.refresh(invoice)
    return invoice

def get_invoice_by_id(invoice_id: int, db: Session):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

def get_all_invoices(db: Session) -> list[Invoice]:
    return db.query(Invoice).all()

def delete_invoice_by_id(invoice_id: int, db: Session) -> bool:
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return False

    db.delete(invoice)
    db.commit()
    return True

def update_invoice_by_id(invoice_id: int, data: InvoiceUpdate, db: Session) -> Optional[Invoice]:
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return None

    if data.provider is not None:
        invoice.provider = data.provider
    if data.total is not None:
        invoice.total = data.total
    if data.date is not None:
        invoice.date = data.date

    db.commit()
    db.refresh(invoice)
    return invoice

def update_invoice_items(invoice_id: int, new_items: list[InvoiceItemUpdate], db: Session) -> Optional[Invoice]:
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return None

    # Eliminar los ítems actuales
    db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()

    # Agregar los nuevos ítems
    for item_data in new_items:
        item = InvoiceItem(
            invoice_id=invoice_id,
            description=item_data.description,
            quantity=item_data.quantity,
            price=item_data.price
        )
        db.add(item)

    db.commit()
    db.refresh(invoice)
    return invoice
