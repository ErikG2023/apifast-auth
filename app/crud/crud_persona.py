from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models.persona import Persona
from app.schemas.persona import PersonaCreacionSchema, PersonaActualizacionSchema
from datetime import datetime

def crear_persona(db: Session, persona: PersonaCreacionSchema, creado_por: int):
    # Verificar si existe el email
    db_persona = db.query(Persona).filter(
        Persona.email == persona.email,
        Persona.eliminado_en.is_(None)
    ).first()
    if db_persona:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
        
    # Verificar si existe el RUT
    db_persona = db.query(Persona).filter(
        Persona.rut == persona.rut,
        Persona.eliminado_en.is_(None)
    ).first()
    if db_persona:
        raise HTTPException(status_code=400, detail="El RUT ya está registrado")

    nueva_persona = Persona(**persona.model_dump(), creado_por=creado_por)
    db.add(nueva_persona)
    db.commit()
    db.refresh(nueva_persona)
    return nueva_persona

def obtener_persona(db: Session, persona_id: int):
    return db.query(Persona).filter(Persona.id == persona_id, Persona.eliminado_en.is_(None)).first()

def listar_personas(db: Session, skip: int = 0, limit: int = 100):
    total = db.query(func.count(Persona.id)).filter(Persona.eliminado_en.is_(None)).scalar()
    personas = db.query(Persona).filter(Persona.eliminado_en.is_(None)).offset(skip).limit(limit).all()
    return personas, total

def listar_personas_eliminadas(db: Session, skip: int = 0, limit: int = 100):
    total = db.query(func.count(Persona.id)).filter(Persona.eliminado_en.isnot(None)).scalar()
    personas = db.query(Persona).filter(Persona.eliminado_en.isnot(None)).offset(skip).limit(limit).all()
    return personas, total

def actualizar_persona(db: Session, persona_id: int, persona: PersonaActualizacionSchema, actualizado_por: int):
    db_persona = db.query(Persona).filter(Persona.id == persona_id, Persona.eliminado_en.is_(None)).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    # Verificar email si se está actualizando
    if persona.email and persona.email != db_persona.email:
        existing_persona = db.query(Persona).filter(
            Persona.email == persona.email,
            Persona.id != persona_id,
            Persona.eliminado_en.is_(None)
        ).first()
        if existing_persona:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Verificar RUT si se está actualizando
    if persona.rut and persona.rut != db_persona.rut:
        existing_persona = db.query(Persona).filter(
            Persona.rut == persona.rut,
            Persona.id != persona_id,
            Persona.eliminado_en.is_(None)
        ).first()
        if existing_persona:
            raise HTTPException(status_code=400, detail="El RUT ya está registrado")
    
    update_data = persona.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_persona, key, value)
    
    db_persona.actualizado_por = actualizado_por
    
    db.commit()
    db.refresh(db_persona)
    return db_persona

def eliminar_persona(db: Session, persona_id: int, eliminado_por: int):
    db_persona = db.query(Persona).filter(Persona.id == persona_id, Persona.eliminado_en.is_(None)).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    db_persona.eliminado_en = func.now()
    db_persona.eliminado_por = eliminado_por
    
    db.commit()
    return db_persona

def restaurar_persona(db: Session, persona_id: int, actualizado_por: int):
    db_persona = db.query(Persona).filter(Persona.id == persona_id, Persona.eliminado_en.isnot(None)).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona eliminada no encontrada")
    
    db_persona.eliminado_en = None
    db_persona.eliminado_por = None
    
    db_persona.actualizado_en = func.now()
    db_persona.actualizado_por = actualizado_por
    
    db.commit()
    db.refresh(db_persona)
    return db_persona