# app/repositories/ventas_repo.py
from app.repositories.base import BaseRepository
from app.models.ventas import Venta

class VentasRepository(BaseRepository[Venta]):
    def __init__(self):
        super().__init__(Venta)
