# app/models/gastos.py
from sqlalchemy import Column, Integer, String, Date, Float, DateTime
from datetime import datetime, date
from app.db.base_class import Base

class Gasto(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, default=date.today, nullable=False)
    comercio = Column(String(200), nullable=False)
    detalle = Column(String(300), nullable=False)
    monto = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

