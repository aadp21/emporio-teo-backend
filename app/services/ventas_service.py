# app/services/ventas_service.py
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.repositories.ventas_repo import VentasRepository
from app.schemas.ventas import VentaCreate
from app.models.ventas import Venta

class VentasService:
    def __init__(self):
        self.repo = VentasRepository()

    def crear(self, db: Session, data: VentaCreate) -> Venta:
        fecha = data.fecha or date.today()
        hora = data.hora or datetime.now().time()
        obj = {
            "fecha": fecha,
            "hora": hora,
            "total": data.total,
            "tipo_pago": data.tipo_pago
        }
        return self.repo.create(db, obj)

    def listar(self, db: Session, skip=0, limit=100):
        return self.repo.get_multi(db, skip=skip, limit=limit)

    def ventas_del_dia(self, db: Session, fecha: date):
        # equivalente a tu filtro df[df['fecha'] == fecha_hoy]
        return db.query(Venta).filter(Venta.fecha == fecha).all()
