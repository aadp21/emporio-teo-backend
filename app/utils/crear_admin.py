# app/utils/crear_admin.py

from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.usuario import Usuario


def crear_admin():
    db = SessionLocal()

    # ⚠️ EDITA ESTOS DATOS ANTES DE EJECUTAR
    nombre = "Administrador"
    email = "teo.market23@gmail.com"
    username = "admin"
    password = "123456"  # cámbialo después en Swagger

    # ¿Existe ya un admin?
    existente = db.query(Usuario).filter(Usuario.username == username).first()
    if existente:
        print("❌ Ya existe un usuario con ese username.")
        return

    user = Usuario(
        nombre=nombre,
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        role="admin",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print("✅ Usuario administrador creado correctamente:")
    print(f"ID: {user.id}")
    print(f"Username: {user.username}")
    print(f"Password temporal: {password}")


if __name__ == "__main__":
    crear_admin()
