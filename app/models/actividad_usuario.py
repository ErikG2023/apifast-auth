from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from app.core.database import Base

class ActividadUsuario(Base):
    __tablename__ = "actividad_usuario"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    tipo_actividad = Column(String(50), nullable=False)
    descripcion = Column(Text)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    direccion_ip = Column(String(45))
    agente_usuario = Column(Text)
    endpoint = Column(String(255))