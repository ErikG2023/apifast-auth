from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.auditable import Auditable

class Persona(Base, Auditable):
    __tablename__ = "persona"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    fecha_nacimiento = Column(Date)
    email = Column(String, unique=True, index=True)
    rut = Column(String(12), unique=True, index=True)
    
    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="persona", uselist=False)