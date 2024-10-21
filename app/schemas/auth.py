from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional

class PermisoRespuesta(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class RolRespuesta(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    permisos: List[PermisoRespuesta]

    class Config:
        from_attributes = True

class UsuarioRespuesta(BaseModel):
    id: int
    nombre_usuario: str
    esta_activo: bool
    es_superusuario: bool
    nombre: str
    apellido: str
    fecha_nacimiento: date
    email: EmailStr
    rol: RolRespuesta

    class Config:
        from_attributes = True

class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    nombre_usuario: str | None = None