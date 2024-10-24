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

def calcular_digito_verificador(numero_rut: str) -> str:
    """
    Calcula el dígito verificador de un RUT chileno.
    """
    serie = [2, 3, 4, 5, 6, 7]
    suma = 0
    
    for i, digit in enumerate(reversed(numero_rut)):
        suma += int(digit) * serie[i % len(serie)]
    
    resto = suma % 11
    dv = 11 - resto
    
    if dv == 11:
        return '0'
    elif dv == 10:
        return 'K'
    else:
        return str(dv)

def generar_rut_valido() -> str:
    """
    Genera un RUT chileno válido aleatorio.
    """
    # Generar número de RUT aleatorio entre 7.000.000 y 25.000.000
    numero = random.randint(7000000, 25000000)
    numero_str = str(numero)
    dv = calcular_digito_verificador(numero_str)
    return f"{numero_str}-{dv}"

def reset_database():
    # Lista de tablas en orden de eliminación
    tables = ['sesion_usuario','usuario', 'rol_permiso', 'persona', 'rol', 'permiso']
    
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
        rut="11111111-1",  # RUT fijo para el admin
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
        rol_id=admin_rol.id,
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
    
    # Mantener un conjunto de RUTs generados para evitar duplicados
    ruts_generados = set()
    
    personas_adicionales = []
    for _ in range(30):
        # Generar un RUT único
        while True:
            rut = generar_rut_valido()
            if rut not in ruts_generados:
                ruts_generados.add(rut)
                break
        
        persona = Persona(
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=80),
            email=fake.email(),
            rut=rut,
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