# app/schemas/ventas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

class VentaBase(BaseModel):
    total: float
    tipo_pago: str

class VentaCreate(VentaBase):
    # opcionalmente permitir fecha/hora desde el front
    fecha: Optional[date] = None
    hora: Optional[time] = None

class VentaRead(VentaBase):
    id: int
    fecha: date
    hora: time

    class Config:
        from_attributes = True
