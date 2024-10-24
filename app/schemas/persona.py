from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime
from typing import Optional
from app.schemas.paginacion import PaginacionBase
from app.utils.rut_util import validar_rut, formatear_rut
from fastapi import HTTPException

class PersonaBase(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    email: EmailStr
    rut: str
    
    @field_validator('rut')
    @classmethod
    def validar_formato_rut(cls, v: str) -> str:
        if not validar_rut(v):
            raise HTTPException(
                status_code=400,
                detail="RUT no válido"
            )
        return formatear_rut(v)

class PersonaCreacionSchema(PersonaBase):
    pass

class PersonaActualizacionSchema(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    email: Optional[EmailStr] = None
    rut: Optional[str] = None
    
    @field_validator('rut')
    @classmethod
    def validar_formato_rut(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not validar_rut(v):
            raise HTTPException(
                status_code=400,
                detail="RUT no válido"
            )
        return formatear_rut(v)

class PersonaRespuestaSchema(PersonaBase):
    id: int
    creado_en: Optional[datetime]
    creado_por: Optional[int]
    actualizado_en: Optional[datetime]
    actualizado_por: Optional[int]

    class Config:
        from_attributes = True

class PersonaPaginada(PaginacionBase[PersonaRespuestaSchema]):
    pass