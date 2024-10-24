from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.actividad_usuario import ActividadUsuario
from app.core.auth import get_current_user
from app.core.config import settings

class ActividadMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Prefijos de rutas a excluir
        prefijos_excluidos = [
            "/docs",
            "/openapi.json",
            f"{settings.API_V1_STR}/authentication/"
        ]
        
        # Verificar si la ruta actual comienza con alguno de los prefijos excluidos
        if any(request.url.path.startswith(prefijo) for prefijo in prefijos_excluidos):
            return await call_next(request)

        response = await call_next(request)

        # Solo registrar actividad para respuestas exitosas
        if 200 <= response.status_code < 400:
            db = SessionLocal()
            try:
                usuario = await get_current_user(request, db)
                
                # Obtener la entidad y la acción del path
                path_parts = request.url.path.split("/")
                entidad = path_parts[3] if len(path_parts) > 3 else "desconocida"
                accion = self.obtener_accion(request.method, path_parts)
                
                descripcion = f"{accion.capitalize()} de {entidad}"
                if len(path_parts) > 4 and path_parts[4].isdigit():
                    descripcion += f" (ID: {path_parts[4]})"
                
                nueva_actividad = ActividadUsuario(
                    usuario_id=usuario.id,
                    tipo_actividad=f"{request.method}_{entidad}",
                    descripcion=descripcion,
                    direccion_ip=request.client.host,
                    agente_usuario=request.headers.get("user-agent"),
                    endpoint=request.url.path
                )
                db.add(nueva_actividad)
                db.commit()
            except Exception as e:
                # Log the error, but don't interrupt the response
                print(f"Error registering activity: {e}")
            finally:
                db.close()

        return response

    def obtener_accion(self, method, path_parts):
        if method == "GET":
            return "consulta" if len(path_parts) > 4 else "listado"
        elif method == "POST":
            return "restauración" if path_parts[-1] == "restaurar" else "creación"
        elif method == "PUT":
            return "actualización"
        elif method == "DELETE":
            return "eliminación"
        else:
            return "acción desconocida"