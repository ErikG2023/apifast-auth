from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Union, Dict, Any
from pydantic import ValidationError

class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

def create_error_response(status_code: int, detail: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    # Si detail es una lista o diccionario, lo dejamos como está
    if isinstance(detail, (list, dict)):
        formatted_detail = detail
    # Si es una excepción, convertimos su mensaje a string
    elif isinstance(detail, Exception):
        formatted_detail = str(detail)
    # Si es un string, lo dejamos como está
    else:
        formatted_detail = detail

    return {
        "error": {
            "status_code": status_code,
            "detail": formatted_detail
        }
    }

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=create_error_response(exc.status_code, exc.detail)
        )
    elif isinstance(exc, StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=create_error_response(exc.status_code, exc.detail)
        )
    elif isinstance(exc, RequestValidationError):
        errors = []
        for error in exc.errors():
            error_detail = {
                "loc": error.get("loc", []),
                "msg": error.get("msg", ""),
                "type": error.get("type", "")
            }
            if "ctx" in error:
                error_detail["ctx"] = error["ctx"]
            errors.append(error_detail)
            
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=create_error_response(status.HTTP_422_UNPROCESSABLE_ENTITY, errors)
        )
    elif isinstance(exc, ValueError):
        # Manejar específicamente los errores de ValueError (como los de validación de RUT)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=create_error_response(
                status.HTTP_400_BAD_REQUEST,
                str(exc)
            )
        )
    else:
        # Para excepciones no manejadas, devolver un error 500
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=create_error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Se ha producido un error interno del servidor"
            )
        )