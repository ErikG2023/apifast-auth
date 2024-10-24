from sqlalchemy.orm import Session
from fastapi import Request
from app.models.actividad_usuario import ActividadUsuario
from app.schemas.auth import UsuarioRespuesta

async def registrar_actividad(
    db: Session,
    usuario: UsuarioRespuesta,
    request: Request,
    tipo_actividad: str,
    descripcion: str
):
    nueva_actividad = ActividadUsuario(
        usuario_id=usuario.id,
        tipo_actividad=tipo_actividad,
        descripcion=descripcion,
        direccion_ip=request.client.host,
        agente_usuario=request.headers.get("user-agent"),
        endpoint=request.url.path
    )
    db.add(nueva_actividad)
    db.commit()