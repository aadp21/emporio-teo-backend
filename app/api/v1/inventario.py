# app/api/v1/inventario.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.inventario import InventarioCreate, InventarioRead, InventarioUpdate
from app.services.inventario_service import InventarioService

router = APIRouter()
service = InventarioService()

@router.get("/inventario", response_model=List[InventarioRead])
def listar_inventario(db: Session = Depends(get_db)):
    return service.listar(db)

@router.post("/inventario", response_model=InventarioRead)
def crear_producto(data: InventarioCreate, db: Session = Depends(get_db)):
    return service.crear_producto(db, data)

@router.put("/inventario/{id}", response_model=InventarioRead)
def actualizar_producto(id: int, data: InventarioUpdate, db: Session = Depends(get_db)):
    return service.actualizar(db, id, data)
