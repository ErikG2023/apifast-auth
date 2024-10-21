from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.auditable import Auditable

class Permiso(Base, Auditable):
    __tablename__ = "permiso"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, index=True)
    descripcion = Column(Text)

    roles = relationship("Rol", secondary="rol_permiso", back_populates="permisos")