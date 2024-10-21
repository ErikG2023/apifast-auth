from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # Ajusta esto según tus necesidades
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Tu API",
        version="1.0.0",
        description="Descripción de tu API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if openapi_schema["paths"][path][method].get("operationId") not in ["login_for_access_token", "root"]:
                openapi_schema["paths"][path][method]["security"] = [{"Bearer Auth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def setup_app_config(app):
    setup_cors(app)
    app.openapi = lambda: custom_openapi(app)