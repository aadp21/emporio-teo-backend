# app/models/ventas.py
from sqlalchemy import Column, Integer, Date, Time, Float, String, DateTime
from datetime import datetime, date, time
from app.db.base_class import Base


def hora_actual():
    """Retorna la hora exacta sin microsegundos."""
    now = datetime.now()
    return time(now.hour, now.minute, now.second)


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, default=date.today, index=True)
    hora = Column(Time, default=hora_actual)
    total = Column(Float, nullable=False)
    tipo_pago = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


