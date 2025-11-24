# app/db/base.py
"""
Base declarativa única para todo el proyecto.
Alembic y SQLAlchemy usan este archivo para detectar todas las tablas.
"""

from app.db.base_class import Base

# Importar todos los modelos SOLO para registro de metadata
from app.models.inventario import Inventario  # noqa
from app.models.ventas import Venta  # noqa
from app.models.gastos import Gasto  # noqa
from app.models.detalle_venta import DetalleVenta  # noqa
from app.models.usuario import Usuario  # noqa  # 👈 aquí solo se importa, no se define




