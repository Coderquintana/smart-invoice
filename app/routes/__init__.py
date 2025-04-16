from fastapi import APIRouter
from app.routes import invoice

api_router = APIRouter()

# Agregá aquí todos tus routers
api_router.include_router(invoice.router)
