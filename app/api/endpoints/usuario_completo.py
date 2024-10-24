import math
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.auth import get_current_user
from app.core.database import get_db
from app.schemas import UsuarioCompletoCreacionSchema, UsuarioCompletoRespuestaSchema
from app.crud import crud_usuario_completo
from app.core.permissions import require_permissions
from app.schemas.auth import UsuarioRespuesta
from app.schemas.usuario_completo import UsuarioCompletoActualizacionSchema, UsuarioCompletoPaginado

router = APIRouter()

@router.post("/", response_model=UsuarioCompletoRespuestaSchema)
@require_permissions("usuario:crear")
async def crear_usuario_completo(
    usuario: UsuarioCompletoCreacionSchema,
    db: Session = Depends(get_db),
    current_user: UsuarioRespuesta = Depends(get_current_user)
):
    return crud_usuario_completo.crear_usuario_completo(
        db=db, 
        usuario_data=usuario, 
        creado_por=current_user.id
    )

@router.get("/{usuario_id}", response_model=UsuarioCompletoRespuestaSchema,)
@require_permissions("usuario:leer")
async def obtener_usuario_completo(usuario_id: int, db: Session = Depends(get_db),current_user: UsuarioRespuesta = Depends(get_current_user)):
    db_usuario = crud_usuario_completo.obtener_usuario_completo(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.get("/", response_model=UsuarioCompletoPaginado)
@require_permissions("usuario:leer")
async def listar_usuarios_completos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UsuarioRespuesta = Depends(get_current_user)
):
    usuarios, total = crud_usuario_completo.listar_usuarios_completos(db, skip=skip, limit=limit)
    
    total_pages = max(1, math.ceil(total / limit))
    current_page = min(skip // limit + 1, total_pages)
    
    return UsuarioCompletoPaginado(
        total=total,
        page=current_page,
        pages=total_pages,
        limit=limit,
        prev_page=current_page - 1 if current_page > 1 else None,
        next_page=current_page + 1 if current_page < total_pages else None,
        items=usuarios
    )

@router.put("/{usuario_id}", response_model=UsuarioCompletoRespuestaSchema)
@require_permissions("usuario:actualizar")
async def actualizar_usuario_completo(
    usuario_id: int,
    usuario: UsuarioCompletoActualizacionSchema,
    db: Session = Depends(get_db),
    current_user: UsuarioRespuesta = Depends(get_current_user)
):
    return crud_usuario_completo.actualizar_usuario_completo(
        db=db, 
        usuario_id=usuario_id, 
        usuario_data=usuario,
        actualizado_por=current_user.id
    )
