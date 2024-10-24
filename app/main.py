from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import auth, usuario_completo, persona
from app.core.app_config import setup_app_config
from app.core.error_handling import global_exception_handler, AppException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.middleware.actividad_middleware import ActividadMiddleware

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

setup_app_config(app)

# Registrar el manejador de excepciones global
app.add_exception_handler(AppException, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.add_middleware(ActividadMiddleware)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/authentication", tags=["auth"])
app.include_router(usuario_completo.router, prefix=f"{settings.API_V1_STR}/usuario-completo", tags=["usuario-completo"])
app.include_router(persona.router, prefix=f"{settings.API_V1_STR}/personas", tags=["personas"])



@app.get("/")
async def root():
    return {"message": "Hello World"}