from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from .auditable import Auditable

class Rol(Base, Auditable):
    __tablename__ = "rol"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, index=True)
    descripcion = Column(Text)

    # Actualizamos la relación con Usuario
    usuarios = relationship("Usuario", back_populates="rol")
    permisos = relationship("Permiso", secondary="rol_permiso", back_populates="roles")