from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_list = []

    for err in errors:
        loc = ".".join([str(l) for l in err["loc"]])
        msg = err["msg"]
        error_list.append({"campo": loc, "error": msg})

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Error de validación",
            "errores": error_list
        }
    )
