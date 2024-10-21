from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

class Auditable:
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    creado_por = Column(Integer, nullable=True)
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())
    actualizado_por = Column(Integer, nullable=True)
    eliminado_en = Column(DateTime(timezone=True), nullable=True)  # Cambiado de Integer a DateTime
    eliminado_por = Column(Integer, nullable=True)