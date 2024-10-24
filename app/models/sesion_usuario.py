from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class SesionUsuario(Base):
    __tablename__ = "sesion_usuario"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    token_sesion = Column(String(255), unique=True, index=True)
    direccion_ip = Column(String(45))
    agente_usuario = Column(String(255))
    inicio_sesion = Column(DateTime)
    fin_sesion = Column(DateTime, nullable=True)

    usuario = relationship("Usuario", back_populates="sesiones")