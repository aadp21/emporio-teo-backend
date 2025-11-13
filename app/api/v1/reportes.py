# app/api/v1/reportes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.db.session import get_db
from app.models.ventas import Venta

router = APIRouter()

@router.get("/reportes/ventas-diarias")
def reporte_ventas_diarias(fecha: date = date.today(), db: Session = Depends(get_db)):
    ventas = db.query(Venta).filter(Venta.fecha == fecha).all()
    if not ventas:
        return {
            "fecha": fecha,
            "total_dia": 0,
            "detalle": []
        }
    total_dia = sum(v.total for v in ventas)
    detalle = [
        {
            "hora": v.hora.strftime("%H:%M:%S"),
            "total": v.total,
            "tipo_pago": v.tipo_pago
        }
        for v in ventas
    ]
    return {
        "fecha": fecha,
        "total_dia": total_dia,
        "detalle": detalle
    }
