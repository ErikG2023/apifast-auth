from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.core.database import get_db
from app.schemas.persona import PersonaCreacionSchema, PersonaRespuestaSchema, PersonaActualizacionSchema, PersonaPaginada
from app.crud import crud_persona
from app.core.permissions import require_permissions
from app.schemas.auth import UsuarioRespuesta

router = APIRouter()

@router.post("/", response_model=PersonaRespuestaSchema)
@require_permissions("persona:crear")
async def crear_persona(
    persona: PersonaCreacionSchema,
    db: Session = Depends(get_db),
    current_user: UsuarioRespuesta = Depends(get_current_user)
):
    return crud_persona.crear_persona(db=db, persona=persona, creado_por=current_user.id)

@router.get("/{persona_id}", response_model=PersonaRespuestaSchema)
@require_permissions("persona:leer")
async def obtener_persona(
    persona_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioRespuesta = Depends(get_current_user)
):
    db_persona = crud_persona.obtener_persona(db, persona_id=persona_id)
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return db_persona

@router.get("/", response_model=PersonaPaginada)
@require_permissions("persona:leer")
async def listar_personas(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UsuarioRespuesta = Depends(get_current_user)
):
    personas, total = crud_persona.listar_personas(db, skip=skip, limit=limit)
    return PersonaPaginada(
        total=total,
        page=skip // limit + 1,
        pages=(total + limit - 1) // limit,
        limit=limit,
        prev_page=skip // limit if skip > 0 else None,
        next_page=skip // limit + 2 if skip + limit < total else None,
        items=personas
    )

@router.put("/{persona_id}", response_model=PersonaRespuestaSchema)
@require_permissions("persona:actualizar")
async def actualizar_persona(
    persona_id: int,
    persona: PersonaActualizacionSchema,
    db: Session = Depends(get_db),
    current_user: UsuarioRespuesta = Depends(get_current_user)
):
    return crud_persona.actualizar_persona(
        db=db,
        persona_id=persona_id,
        persona=persona,
        actualizado_por=current_user.id
    )

@router.delete("/{persona_id}", response_model=PersonaRespuestaSchema)
@require_permissions("persona:eliminar")
async def eliminar_persona(
    persona_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioRespuesta = Depends(get_current_user)
):
    return crud_persona.eliminar_persona(
        db=db,
        persona_id=persona_id,
        eliminado_por=current_user.id
    )

@router.post("/{persona_id}/restaurar", response_model=PersonaRespuestaSchema)
@require_permissions("persona:restaurar")
async def restaurar_persona(
    persona_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioRespuesta = Depends(get_current_user)
):
    return crud_persona.restaurar_persona(db=db, persona_id=persona_id, actualizado_por=current_user.id)