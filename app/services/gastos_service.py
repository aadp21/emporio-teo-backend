# app/services/gastos_service.py
from sqlalchemy.orm import Session
from app.repositories.gastos_repo import GastosRepository
from app.schemas.gastos import GastoCreate
from datetime import date

class GastosService:
    def __init__(self):
        self.repo = GastosRepository()

    def crear(self, db: Session, data: GastoCreate):
        return self.repo.create(db, data.model_dump())

    def listar(self, db: Session, fecha: date | None = None):
        if fecha:
            # filtrado simple
            from app.models.gastos import Gasto
            return db.query(Gasto).filter(Gasto.fecha == fecha).all()
        return self.repo.get_multi(db)
