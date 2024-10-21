from sqlalchemy import Column, ForeignKey, Integer
from app.core.database import Base
from app.models.auditable import Auditable

class RolPermiso(Base, Auditable):
    __tablename__ = "rol_permiso"

    rol_id = Column(Integer, ForeignKey("rol.id"), primary_key=True)
    permiso_id = Column(Integer, ForeignKey("permiso.id"), primary_key=True)