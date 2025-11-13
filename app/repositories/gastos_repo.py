# app/repositories/gastos_repo.py
from app.repositories.base import BaseRepository
from app.models.gastos import Gasto

class GastosRepository(BaseRepository[Gasto]):
    def __init__(self):
        super().__init__(Gasto)
