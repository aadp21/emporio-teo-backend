# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1 import inventario, ventas, gastos, reportes, auth
from app.web import routes as web_routes

app = FastAPI(title="Emporio Teo - API")

# Rutas API
app.include_router(inventario.router, prefix="/api/v1", tags=["inventario"])
app.include_router(ventas.router, prefix="/api/v1", tags=["ventas"])
app.include_router(gastos.router, prefix="/api/v1", tags=["gastos"])
app.include_router(reportes.router, prefix="/api/v1", tags=["reportes"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

# Rutas WEB
app.include_router(web_routes.router, tags=["web"])

# Archivos estáticos (para imágenes, iconos, estilos, etc)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return {"msg": "Emporio Teo API funcionando"}

