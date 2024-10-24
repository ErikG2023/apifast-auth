from pydantic import BaseModel
from typing import Optional

class RolCreacionSchema(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolRespuestaSchema(RolCreacionSchema):
    id: int

    class Config:
        from_attributes = True