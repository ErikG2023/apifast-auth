from datetime import date
from typing import Optional
from pydantic import BaseModel

from app.schemas.paginacion import PaginacionBase
from .persona import PersonaCreacionSchema, PersonaRespuestaSchema
from .rol import RolRespuestaSchema
from .usuario import UsuarioCreacionSchema, UsuarioRespuestaSchema

# CREACION
class UsuarioCompletoCreacionSchema(BaseModel):
    persona: PersonaCreacionSchema
    usuario: UsuarioCreacionSchema
    rol_id: int

class UsuarioCompletoRespuestaSchema(UsuarioRespuestaSchema):
    persona: PersonaRespuestaSchema
    rol: RolRespuestaSchema
    creado_por: Optional[int] = None
    actualizado_por: Optional[int] = None
    
# ACTUALIZACION
class PersonaActualizacionSchema(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    rut: Optional[str] = None

class UsuarioActualizacionSchema(BaseModel):
    esta_activo: Optional[bool] = None
    es_superusuario: Optional[bool] = None

class UsuarioCompletoActualizacionSchema(BaseModel):
    persona: Optional[PersonaActualizacionSchema] = None
    usuario: Optional[UsuarioActualizacionSchema] = None
    rol_id: Optional[int] = None
    
# PAGINACION
class UsuarioCompletoPaginado(PaginacionBase[UsuarioCompletoRespuestaSchema]):
    pass