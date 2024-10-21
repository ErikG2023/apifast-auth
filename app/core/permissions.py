from functools import wraps
from fastapi import HTTPException, Depends
from app.core.auth import get_current_user
from app.schemas.auth import UsuarioRespuesta

def require_permissions(*required_permissions):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: UsuarioRespuesta = Depends(get_current_user), **kwargs):
            if current_user.es_superusuario:
                return await func(*args, current_user=current_user, **kwargs)
            
            user_permissions = set(permiso.nombre for permiso in current_user.rol.permisos)
            
            if not set(required_permissions).issubset(user_permissions):
                raise HTTPException(status_code=403, detail="No tienes permisos suficientes para realizar esta acción")
            
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator