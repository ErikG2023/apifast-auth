from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Union, Dict, Any

class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

def create_error_response(status_code: int, detail: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "error": {
            "status_code": status_code,
            "detail": detail
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
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=create_error_response(status.HTTP_422_UNPROCESSABLE_ENTITY, exc.errors())
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