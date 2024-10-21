from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password
from app.crud import crud_auth
from app.core.database import get_db
from app.schemas.auth import TokenPayload, UsuarioRespuesta, RolRespuesta, PermisoRespuesta

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request, db: Session = Depends(get_db)) -> UsuarioRespuesta:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = await get_token_from_request(request)
    if not token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        nombre_usuario: str = payload.get("sub")
        if nombre_usuario is None:
            raise credentials_exception
        token_data = TokenPayload(nombre_usuario=nombre_usuario)
    except JWTError:
        raise credentials_exception
    user = crud_auth.get_by_nombre_usuario(db, nombre_usuario=token_data.nombre_usuario)
    if user is None:
        raise credentials_exception
    
    rol = user.rol
    return UsuarioRespuesta(
        id=user.id,
        nombre_usuario=user.nombre_usuario,
        esta_activo=user.esta_activo,
        es_superusuario=user.es_superusuario,
        nombre=user.persona.nombre,
        apellido=user.persona.apellido,
        fecha_nacimiento=user.persona.fecha_nacimiento,
        email=user.persona.email,
        rol=RolRespuesta(
            id=rol.id,
            nombre=rol.nombre,
            descripcion=rol.descripcion,
            permisos=[PermisoRespuesta(
                id=permiso.id,
                nombre=permiso.nombre,
                descripcion=permiso.descripcion
            ) for permiso in rol.permisos]
        ) if rol else None
    )

def authenticate_user(db: Session, username: str, password: str):
    user = crud_auth.get_by_nombre_usuario(db, nombre_usuario=username)
    if not user:
        return False
    if not verify_password(password, user.hash_contrasena):
        return False
    return user

async def get_token_from_request(request: Request) -> str | None:
    token = request.cookies.get("access_token")
    if token and token.startswith("Bearer "):
        return token.split("Bearer ")[1]
    return token