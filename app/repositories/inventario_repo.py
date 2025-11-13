# app/repositories/inventario_repo.py
from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base import BaseRepository
from app.models.inventario import Inventario

class InventarioRepository(BaseRepository[Inventario]):
    def __init__(self):
        super().__init__(Inventario)

    def get_by_codigo(self, db: Session, codigo: str) -> Optional[Inventario]:
        return db.query(Inventario).filter(Inventario.codigo == codigo).first()
