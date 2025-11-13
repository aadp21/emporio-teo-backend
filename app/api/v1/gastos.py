# app/api/v1/gastos.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.db.session import get_db
from app.schemas.gastos import GastoCreate, GastoRead
from app.services.gastos_service import GastosService

router = APIRouter()
service = GastosService()

@router.get("/gastos", response_model=List[GastoRead])
def listar_gastos(fecha: Optional[date] = None, db: Session = Depends(get_db)):
    return service.listar(db, fecha=fecha)

@router.post("/gastos", response_model=GastoRead)
def crear_gasto(data: GastoCreate, db: Session = Depends(get_db)):
    return service.crear(db, data)
