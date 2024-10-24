from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.schemas.auth import TokenRespuesta, UsuarioRespuesta
from app.core.auth import create_access_token, get_current_user, authenticate_user
from app.core.error_handling import AppException
from datetime import timedelta

from app.utils.sesion_util import registrar_fin_sesion, registrar_inicio_sesion

router = APIRouter()

@router.post("/login", response_model=TokenRespuesta)
async def login_for_access_token(
    response: Response,
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    if not user.esta_activo:
        raise AppException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nombre_usuario}, expires_delta=access_token_expires
    )
    
    # Registrar el inicio de sesión
    registrar_inicio_sesion(db, user.id, access_token, request)
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite='lax',
        secure=False  # Set to True in production with HTTPS
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if token and token.startswith("Bearer "):
        token = token.split("Bearer ")[1]
        registrar_fin_sesion(db, token)
    
    response.delete_cookie(key="access_token")
    return {"message": "Sesión cerrada exitosamente"}

@router.get("/me", response_model=UsuarioRespuesta)
async def read_users_me(current_user: UsuarioRespuesta = Depends(get_current_user)):
    return current_user