# app/models/detalle_venta.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from app.db.base_class import Base

class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id", ondelete="CASCADE"), nullable=False)
    inventario_id = Column(Integer, ForeignKey("inventario.id", ondelete="SET NULL"))
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Float, nullable=False, default=0)

