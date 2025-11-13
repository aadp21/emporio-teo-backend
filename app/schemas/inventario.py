# app/schemas/inventario.py
from pydantic import BaseModel
from typing import Optional

class InventarioBase(BaseModel):
    codigo: str
    nombre: str
    precio: float
    precio_costo: float
    cantidad: int
    stock_estado: Optional[str] = ""

class InventarioCreate(InventarioBase):
    pass

class InventarioUpdate(BaseModel):
    nombre: Optional[str]
    precio: Optional[float]
    precio_costo: Optional[float]
    cantidad: Optional[int]
    stock_estado: Optional[str]

class InventarioRead(InventarioBase):
    id: int

    class Config:
        from_attributes = True
