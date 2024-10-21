from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.core.config import settings
from app.models import Rol, Permiso, Persona, Usuario, RolPermiso
from app.core.security import get_password_hash
from faker import Faker
import random

# Crear el motor de la base de datos
engine = create_engine(settings.DATABASE_URL)

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def reset_database():
    # Lista de tablas en orden de eliminación
    tables = ['usuario', 'rol_permiso', 'persona', 'rol', 'permiso']
    
    # Desactivar temporalmente las restricciones de clave foránea
    db.execute(text("SET CONSTRAINTS ALL DEFERRED"))
    
    # Truncar todas las tablas y reiniciar las secuencias
    for table in tables:
        db.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
    
    # Reactivar las restricciones de clave foránea
    db.execute(text("SET CONSTRAINTS ALL IMMEDIATE"))
    
    db.commit()

    # Insertar roles
    now = datetime.utcnow()
    admin_rol = Rol(
        nombre="admin",
        descripcion="Administrador con todos los permisos",
        creado_en=now,
        actualizado_en=now,
        creado_por=None,
        actualizado_por=None,
        eliminado_en=None,
        eliminado_por=None
    )
    user_rol = Rol(
        nombre="user",
        descripcion="Usuario estándar con permisos limitados",
        creado_en=now,
        actualizado_en=now,
        creado_por=None,
        actualizado_por=None,
        eliminado_en=None,
        eliminado_por=None
    )
    db.add_all([admin_rol, user_rol])
    db.commit()

    # Insertar permisos
    permisos_data = [
        ("permiso:actualizar", "Permite actualizar informacion de permisos"),
        ("permiso:crear", "Permite crear nuevos permisos"),
        ("permiso:eliminar", "Permite eliminar permisos"),
        ("permiso:leer", "Permite ver informacion permisos"),
        ("permiso:restaurar", "Permite restaurar informacion de permisos"),
        ("persona:actualizar", "Permite actualizar informacion de personas"),
        ("persona:crear", "Permite crear nuevas personas"),
        ("persona:eliminar", "Permite eliminar personas"),
        ("persona:leer", "Permite ver informacion de personas"),
        ("persona:restaurar", "Permite restaurar informacion de personas"),
        ("rol:actualizar", "Permite actualizar información de roles"),
        ("rol:crear", "Permite crear nuevos roles"),
        ("rol:eliminar", "Permite eliminar roles"),
        ("rol:leer", "Permite ver información de roles"),
        ("rol:restaurar", "Permite restaurar informacion de roles"),
        ("usuario:actualizar", "Permite actualizar información de usuarios"),
        ("usuario:crear", "Permite crear nuevos usuarios"),
        ("usuario:eliminar", "Permite eliminar usuarios"),
        ("usuario:leer", "Permite ver información de usuarios"),
        ("usuario:restaurar", "Permite restaurar informacion de usuarios")
    ]
    
    permisos = [Permiso(
        nombre=nombre,
        descripcion=desc,
        creado_en=now,
        actualizado_en=now,
        creado_por=None,
        actualizado_por=None,
        eliminado_en=None,
        eliminado_por=None
    ) for nombre, desc in permisos_data]
    db.add_all(permisos)
    db.commit()

    # Asignar todos los permisos al rol admin
    for permiso in permisos:
        db.add(RolPermiso(
            rol_id=admin_rol.id,
            permiso_id=permiso.id,
            creado_en=now,
            actualizado_en=now,
            creado_por=None,
            actualizado_por=None,
            eliminado_en=None,
            eliminado_por=None
        ))
    
    # Asignar permisos de lectura al rol user
    for permiso in permisos:
        if permiso.nombre.endswith(':leer'):
            db.add(RolPermiso(
                rol_id=user_rol.id,
                permiso_id=permiso.id,
                creado_en=now,
                actualizado_en=now,
                creado_por=None,
                actualizado_por=None,
                eliminado_en=None,
                eliminado_por=None
            ))
    
    db.commit()

    # Insertar persona administradora
    admin_persona = Persona(
        nombre="Administrador",
        apellido="Administrador",
        fecha_nacimiento=datetime(1991, 8, 27),
        email="superadmin@gmail.com",
        creado_en=now,
        actualizado_en=now,
        creado_por=None,
        actualizado_por=None,
        eliminado_en=None,
        eliminado_por=None
    )
    db.add(admin_persona)
    db.commit()

    # Insertar usuario administrador
    admin_usuario = Usuario(
        nombre_usuario="admin",
        hash_contrasena=get_password_hash("123456789"),
        esta_activo=True,
        es_superusuario=True,
        persona_id=admin_persona.id,
        rol_id=admin_rol.id,  # Asignamos directamente el rol_id
        creado_en=now,
        actualizado_en=now,
        creado_por=None,
        actualizado_por=None,
        eliminado_en=None,
        eliminado_por=None
    )
    db.add(admin_usuario)
    db.commit()

    print("Base de datos reiniciada y poblada con éxito.")

def agregar_personas_adicionales():
    fake = Faker()
    now = datetime.utcnow()
    
    personas_adicionales = []
    for _ in range(30):
        persona = Persona(
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=80),
            email=fake.email(),
            creado_en=now,
            actualizado_en=now,
            creado_por=None,
            actualizado_por=None,
            eliminado_en=None,
            eliminado_por=None
        )
        personas_adicionales.append(persona)
    
    db.add_all(personas_adicionales)
    db.commit()

    print(f"Se han agregado {len(personas_adicionales)} personas adicionales a la base de datos.")

if __name__ == "__main__":
    reset_database()
    agregar_personas_adicionales()