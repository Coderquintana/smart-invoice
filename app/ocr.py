import pytesseract
from PIL import Image
import io
import re
from datetime import datetime

def extract_text_from_image(file: bytes) -> str:
    image = Image.open(io.BytesIO(file))
    return pytesseract.image_to_string(image)

def parse_invoice_data(text: str) -> dict:
    lines = text.splitlines()
    provider = "Proveedor Desconocido"
    total = 0.0
    date = "2025-01-01"  # valor por defecto

    # 🧾 Proveedor (usamos la primera línea legible)
    for line in lines:
        if len(line.strip()) > 4:
            provider = line.strip()
            break

    # 💰 Buscar el total usando regex
    total_match = re.search(r"total\s*[:\-]?\s*\$?\s*([\d.,]+)", text, re.IGNORECASE)
    if total_match:
        total_str = total_match.group(1).replace(",", ".")
        try:
            total = float(total_str)
        except ValueError:
            pass

    # 📅 Buscar fecha
    date_match = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    if date_match:
        try:
            parsed_date = datetime.strptime(date_match.group(1), "%d/%m/%Y")
            date = parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return {
        "provider": provider,
        "total": total,
        "date": date
    }

def extract_items_from_text(text: str) -> list:
    items = []
    lines = text.splitlines()

    for line in lines:
        # Buscar líneas que tengan al menos 2 números al final
        match = re.match(r"(.+?)\s{1,}(\d+(?:[.,]\d+)?)\s+([\d.,]+)", line)
        if match:
            description = match.group(1).strip()

            try:
                quantity = int(float(match.group(2)))
            except ValueError:
                quantity = 1

            try:
                price = float(match.group(3).replace(",", ".").replace("€", ""))
            except ValueError:
                price = 0.0

            # 🧠 Filtros de validación para evitar errores del OCR
            if (
                description                  # no vacío
                and len(description) > 3     # mínimo 4 letras
                and quantity > 0
                and quantity < 1000          # límite lógico
                and price > 0
                and price < 10_000           # evitar montos delirantes
            ):
                items.append({
                    "description": description,
                    "quantity": quantity,
                    "price": round(price, 2)
                })

    return items

