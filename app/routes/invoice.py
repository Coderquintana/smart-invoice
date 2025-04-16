from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Invoice
from app.schemas import InvoiceCreate
from app.ocr import extract_text_from_image, parse_invoice_data
from app.ocr import extract_items_from_text
from app.models import InvoiceItem


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload-invoice/")
async def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    text = extract_text_from_image(content)
    parsed = parse_invoice_data(text)

    # ejemplo simple de extracción "manual"
    invoice_data = Invoice(provider=parsed["provider"],total=parsed["total"],date=parsed["date"])

    db.add(invoice_data)
    db.commit()       # guarda la factura y genera el ID
    db.refresh(invoice_data)  # asegura que invoice_data.id esté disponible

    items_data = extract_items_from_text(text)

    for item in items_data:
        invoice_item = InvoiceItem(
            invoice_id=invoice_data.id,
            description=item["description"],
            quantity=item["quantity"],
            price=item["price"]
        )
        db.add(invoice_item)
    db.commit()

    return {
    "extracted_text": text,
    "items_detected": items_data,
    "saved_invoice": {
        "id": invoice_data.id,
        "provider": invoice_data.provider,
        "total": invoice_data.total,
        "date": invoice_data.date
    }
}
