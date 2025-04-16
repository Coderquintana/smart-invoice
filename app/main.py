from fastapi import FastAPI
from app.database import Base, engine
from app.routes import api_router
from fastapi.exceptions import RequestValidationError
from app.exceptions.validation_handler import validation_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(api_router)
