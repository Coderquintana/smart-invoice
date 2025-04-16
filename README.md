# 🧠 Smart Invoice

Sistema inteligente de carga y gestión de facturas a partir de imágenes o fotos, usando OCR y FastAPI.

## ⚙️ Tecnologías

- 🐍 Python 3.13
- 🚀 FastAPI
- 📦 SQLAlchemy
- 🧠 Tesseract OCR (temporalmente para lectura de texto en imágenes)
- 🐘 PostgreSQL
- 📄 Pydantic v2
- 📋 Uvicorn para desarrollo local

## 🧠 ¿Qué hace?

Permite subir una imagen con una factura y:

- Extrae texto con OCR.
- Detecta el proveedor, fecha, total e ítems de la factura.
- Guarda los datos estructurados en la base de datos.
- Permite consultar, editar y eliminar facturas e ítems vía endpoints REST.

## 📁 Estructura del proyecto

```
smart-invoice/
├── app/
│   ├── routes/
│   ├── models.py
│   ├── schemas.py
│   ├── services/
│   ├── repositories/
│   ├── ocr.py
│   ├── database.py
│   └── main.py
├── requirements.txt
└── README.md
```

## 🚀 Cómo levantar el proyecto

1. Crear entorno virtual e instalar dependencias:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Correr servidor local:
```bash
uvicorn app.main:app --reload
```

3. Entrar a Swagger:
```
http://localhost:8000/docs
```

## ✅ Endpoints disponibles

- `POST /upload-invoice/`: Cargar factura desde imagen.
- `GET /invoices/{id}`: Obtener factura por ID.
- `DELETE /invoices/{id}`: Eliminar factura.
- `PUT /invoices/{id}/items`: Actualizar ítems de una factura.

> Más endpoints vendrán con la gestión de proveedores, clientes, exportaciones, etc.