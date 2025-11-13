# app/main.py
from fastapi import FastAPI
from app.api.v1 import inventario, ventas, gastos, reportes

app = FastAPI(title="Emporio Teo - API")

app.include_router(inventario.router, prefix="/api/v1", tags=["inventario"])
app.include_router(ventas.router, prefix="/api/v1", tags=["ventas"])
app.include_router(gastos.router, prefix="/api/v1", tags=["gastos"])
app.include_router(reportes.router, prefix="/api/v1", tags=["reportes"])


@app.get("/")
def root():
    return {"msg": "Emporio Teo API funcionando"}