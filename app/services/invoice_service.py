from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models import Invoice
from app.ocr import extract_text_from_image, parse_invoice_data, extract_items_from_text
from app.repositories.invoice_repository import save_invoice_with_items, get_invoice_by_id, get_all_invoices, delete_invoice_by_id, update_invoice_by_id, update_invoice_items
from app.schemas import InvoiceOut, InvoiceUpdate, InvoiceItemsUpdate
from typing import Optional

async def process_invoice(file: UploadFile, db: Session) -> InvoiceOut:
    content = await file.read()
    text = extract_text_from_image(content)
    parsed = parse_invoice_data(text)
    items_data = extract_items_from_text(text)

    invoice = save_invoice_with_items(db, parsed, items_data)

    return InvoiceOut.model_validate(invoice, from_attributes=True)

def fetch_invoice_by_id(invoice_id: int, db: Session):
    return get_invoice_by_id(invoice_id, db)

def fetch_all_invoices(db: Session) -> list[Invoice]:
    return get_all_invoices(db)

def delete_invoice(invoice_id: int, db: Session) -> bool:
    return delete_invoice_by_id(invoice_id, db)

def update_invoice(invoice_id: int, data: InvoiceUpdate, db: Session) -> Optional[Invoice]:
    return update_invoice_by_id(invoice_id, data, db)

def update_items(invoice_id: int, data: InvoiceItemsUpdate, db: Session) -> Optional[Invoice]:
    return update_invoice_items(invoice_id, data.items, db)
