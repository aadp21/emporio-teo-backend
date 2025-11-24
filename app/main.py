# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.api.v1 import inventario, ventas, gastos, reportes, auth
from app.web import routes as web_routes

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.usuario import Usuario
from app.core.security import get_password_hash

app = FastAPI(title="Emporio Teo - API")

# Archivos estáticos (icono, CSS, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Rutas API
app.include_router(inventario.router, prefix="/api/v1", tags=["inventario"])
app.include_router(ventas.router, prefix="/api/v1", tags=["ventas"])
app.include_router(gastos.router, prefix="/api/v1", tags=["gastos"])
app.include_router(reportes.router, prefix="/api/v1", tags=["reportes"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

# Rutas web (panel HTML)
app.include_router(web_routes.router, tags=["web"])


@app.on_event("startup")
def on_startup():
    """
    Este bloque se ejecuta al iniciar la app (local y Render).
    - Crea las tablas que falten (incluida 'usuarios').
    - Crea un usuario admin por defecto si no existe.
    """
    # 1) Crear tablas que falten en la BD (ej: 'usuarios')
    Base.metadata.create_all(bind=engine)

    # 2) Crear usuario admin si no existe
    db = SessionLocal()
    try:
        admin = db.query(Usuario).filter(Usuario.username == "admin").first()
        if not admin:
            admin = Usuario(
                nombre="Administrador",
                email="admin@example.com",
                username="admin",
                hashed_password=get_password_hash("123456"),  # password temporal
                role="admin",
                is_active=True,
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


# Redirigir la raíz directamente al login del panel
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/panel/login")

