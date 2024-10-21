from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.auditable import Auditable

class Usuario(Base, Auditable):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, unique=True, index=True)
    hash_contrasena = Column(String)
    esta_activo = Column(Boolean, default=True)
    es_superusuario = Column(Boolean, default=False)

    persona_id = Column(Integer, ForeignKey("persona.id"))
    persona = relationship("Persona", back_populates="usuario")

    # Cambiamos la relación con Rol
    rol_id = Column(Integer, ForeignKey("rol.id"))
    rol = relationship("Rol", back_populates="usuarios")