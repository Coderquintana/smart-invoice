# 🧾 Smart Invoice

Este es un proyecto backend construido con **FastAPI** que permite procesar facturas en imagen (fotos o escaneos) mediante **OCR con Tesseract**, extraer datos como proveedor, fecha, total e ítems, y guardarlos en una base de datos PostgreSQL.

---

## 🚀 Características principales

- 📸 Carga de imágenes de facturas vía endpoint `/upload-invoice`
- 🧠 Extracción automática de:
  - Texto completo
  - Proveedor
  - Fecha
  - Total
  - Lista de ítems (productos + cantidad + precio)
- 🗄️ Guardado en base de datos relacional PostgreSQL
- 🧪 Documentación automática en `/docs`

---

## 📦 Requisitos

- Python 3.8+
- PostgreSQL
- Tesseract OCR instalado y agregado al PATH

---

## 🛠 Instalación

1. Cloná el repo:
   ```bash
   git clone https://github.com/tu_usuario/smart-invoice.git
   cd smart-invoice
