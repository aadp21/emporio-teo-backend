# app/models/inventario.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from app.db.base_class import Base

class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False, default=0)
    precio_costo = Column(Float, nullable=False, default=0)
    cantidad = Column(Integer, nullable=False, default=0)
    stock_estado = Column(String(50), default="")
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
