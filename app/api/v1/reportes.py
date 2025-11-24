# app/api/v1/reportes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from collections import defaultdict

from app.db.session import get_db
from app.models.ventas import Venta

router = APIRouter()

@router.get("/reportes/ventas-diarias")
def reporte_ventas_diarias(fecha: date = date.today(), db: Session = Depends(get_db)):
    # Obtener todas las ventas del día
    ventas = db.query(Venta).filter(Venta.fecha == fecha).all()

    # Si no hay ventas, devolvemos todo en cero
    if not ventas:
        return {
            "fecha": fecha,
            "total_dia": 0,
            "totales_por_pago": {},
            "detalle": []
        }

    # Total del día (suma de todas las ventas)
    total_dia = sum(v.total for v in ventas)

    # Totales por tipo de pago (efectivo, débito, crédito, etc.)
    totales_por_pago = defaultdict(float)
    for v in ventas:
        # v.tipo_pago es un string (por ejemplo: "Efectivo", "Débito", etc.)
        totales_por_pago[v.tipo_pago] += v.total

    # Detalle por venta (como ya tenías)
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
        "totales_por_pago": dict(totales_por_pago),
        "detalle": detalle
    }

