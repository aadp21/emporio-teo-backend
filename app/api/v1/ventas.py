# app/api/v1/ventas.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.db.session import get_db
from app.schemas.ventas import VentaCreate, VentaRead
from app.services.ventas_service import VentasService

router = APIRouter()
service = VentasService()

@router.get("/ventas", response_model=List[VentaRead])
def listar_ventas(db: Session = Depends(get_db)):
    return service.listar(db)

@router.post("/ventas", response_model=VentaRead)
def crear_venta(data: VentaCreate, db: Session = Depends(get_db)):
    return service.crear(db, data)

@router.get("/ventas/dia", response_model=List[VentaRead])
def ventas_del_dia(fecha: date, db: Session = Depends(get_db)):
    # GET /api/v1/ventas/dia?fecha=2025-11-08
    return service.ventas_del_dia(db, fecha)
