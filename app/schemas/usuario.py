from pydantic import BaseModel

class UsuarioCreacionSchema(BaseModel):
    nombre_usuario: str
    contrasena: str
    esta_activo: bool = True
    es_superusuario: bool = False

class UsuarioRespuestaSchema(BaseModel):
    id: int
    nombre_usuario: str
    esta_activo: bool
    es_superusuario: bool

    class Config:
        from_attributes = True