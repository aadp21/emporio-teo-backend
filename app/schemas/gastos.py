# app/schemas/gastos.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class GastoBase(BaseModel):
    fecha: date
    comercio: str
    detalle: str
    monto: float

class GastoCreate(GastoBase):
    pass

class GastoRead(GastoBase):
    id: int

    class Config:
        from_attributes = True
