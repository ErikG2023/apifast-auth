from sqlalchemy.orm import Session
from app.models.usuario import Usuario


def get_by_nombre_usuario(db: Session, nombre_usuario: str) -> Usuario:
        return db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()