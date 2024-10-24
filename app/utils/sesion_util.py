from sqlalchemy.orm import Session
from app.models.sesion_usuario import SesionUsuario
from fastapi import Request
from datetime import datetime

def registrar_inicio_sesion(db: Session, usuario_id: int, token: str, request: Request) -> SesionUsuario:
    nueva_sesion = SesionUsuario(
        usuario_id=usuario_id,
        token_sesion=token,
        direccion_ip=request.client.host,
        agente_usuario=request.headers.get("user-agent"),
        inicio_sesion=datetime.utcnow()
    )
    db.add(nueva_sesion)
    db.commit()
    db.refresh(nueva_sesion)
    return nueva_sesion

def registrar_fin_sesion(db: Session, token: str) -> bool:
    sesion = db.query(SesionUsuario).filter(SesionUsuario.token_sesion == token).first()
    if sesion:
        sesion.fin_sesion = datetime.utcnow()
        db.commit()
        return True
    return False