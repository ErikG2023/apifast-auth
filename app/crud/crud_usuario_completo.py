from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Usuario, Persona, Rol
from app.schemas import UsuarioCompletoCreacionSchema, UsuarioCompletoRespuestaSchema
from app.core.security import get_password_hash
from fastapi import HTTPException

from app.schemas.usuario_completo import UsuarioCompletoActualizacionSchema

def crear_usuario_completo(db: Session, usuario_data: UsuarioCompletoCreacionSchema, creado_por: int):
    # Verificar si el rol existe
    rol = db.query(Rol).filter(Rol.id == usuario_data.rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    # Verificar si el email ya existe (incluyendo registros eliminados lógicamente)
    if db.query(Persona).filter(
        Persona.email == usuario_data.persona.email,
        Persona.eliminado_en.is_(None)
    ).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Verificar si el RUT ya existe (incluyendo registros eliminados lógicamente)
    if db.query(Persona).filter(
        Persona.rut == usuario_data.persona.rut,
        Persona.eliminado_en.is_(None)
    ).first():
        raise HTTPException(status_code=400, detail="El RUT ya está registrado")

    # Verificar si el nombre de usuario ya existe
    if db.query(Usuario).filter(Usuario.nombre_usuario == usuario_data.usuario.nombre_usuario).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

    # Crear la persona
    nueva_persona = Persona(**usuario_data.persona.model_dump(), creado_por=creado_por)
    db.add(nueva_persona)
    db.flush()

    # Crear el usuario
    nuevo_usuario = Usuario(
        nombre_usuario=usuario_data.usuario.nombre_usuario,
        hash_contrasena=get_password_hash(usuario_data.usuario.contrasena),
        esta_activo=usuario_data.usuario.esta_activo,
        es_superusuario=usuario_data.usuario.es_superusuario,
        persona_id=nueva_persona.id,
        rol_id=usuario_data.rol_id,
        creado_por=creado_por
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario

def actualizar_usuario_completo(
    db: Session, 
    usuario_id: int, 
    usuario_data: UsuarioCompletoActualizacionSchema,
    actualizado_por: int
):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar datos de la persona
    if usuario_data.persona:
        persona_data = usuario_data.persona.model_dump(exclude_unset=True)
        
        # Verificar unicidad del RUT si se está actualizando
        if 'rut' in persona_data:
            existing_rut = db.query(Persona).filter(
                Persona.rut == persona_data['rut'],
                Persona.id != db_usuario.persona_id,
                Persona.eliminado_en.is_(None)
            ).first()
            if existing_rut:
                raise HTTPException(status_code=400, detail="El RUT ya está registrado")
                
        for key, value in persona_data.items():
            setattr(db_usuario.persona, key, value)
        db_usuario.persona.actualizado_por = actualizado_por

    # Actualizar datos del usuario
    if usuario_data.usuario:
        for key, value in usuario_data.usuario.model_dump(exclude_unset=True).items():
            setattr(db_usuario, key, value)
    
    # Actualizar rol si se proporciona
    if usuario_data.rol_id is not None:
        rol = db.query(Rol).filter(Rol.id == usuario_data.rol_id).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        db_usuario.rol_id = usuario_data.rol_id

    db_usuario.actualizado_por = actualizado_por

    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuario_completo(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def listar_usuarios_completos(db: Session, skip: int = 0, limit: int = 100):
    total = db.query(func.count(Usuario.id)).scalar()
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios, total