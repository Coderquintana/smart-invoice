from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.invoice_service import fetch_all_invoices, process_invoice, fetch_invoice_by_id, delete_invoice, update_invoice, update_items
from app.schemas import InvoiceOut, InvoiceUpdate, InvoiceItemsUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload-invoice/", response_model=InvoiceOut)
async def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await process_invoice(file, db)

@router.get("/invoices/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = fetch_invoice_by_id(invoice_id, db)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.get("/invoices", response_model=list[InvoiceOut])
def list_invoices(db: Session = Depends(get_db)):
    return fetch_all_invoices(db)

@router.delete("/invoices/{invoice_id}")
def delete_invoice_endpoint(invoice_id: int, db: Session = Depends(get_db)):
    deleted = delete_invoice(invoice_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return JSONResponse(content={"message": f"Invoice {invoice_id} deleted successfully"})

@router.put("/invoices/{invoice_id}", response_model=InvoiceOut)
def update_invoice_endpoint(invoice_id: int, data: InvoiceUpdate, db: Session = Depends(get_db)):
    updated = update_invoice(invoice_id, data, db)
    if not updated:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return InvoiceOut.model_validate(updated, from_attributes=True)

from app.schemas import InvoiceItemsUpdate

@router.put("/invoices/{invoice_id}/items", response_model=InvoiceOut)
def update_invoice_items_endpoint(invoice_id: int, data: InvoiceItemsUpdate, db: Session = Depends(get_db)):
    updated_invoice = update_items(invoice_id, data, db)
    if not updated_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return InvoiceOut.model_validate(updated_invoice, from_attributes=True)
