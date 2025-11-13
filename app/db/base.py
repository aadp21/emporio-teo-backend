# app/db/base.py
"""
Base declarativa y registro de modelos principales del sistema Emporio Teo.
Este archivo es leído por Alembic para detectar las tablas que deben crearse
en la base de datos durante las migraciones.
"""

from sqlalchemy.orm import declarative_base
# app/db/base.py
from app.db.base_class import Base

# Importar todos los modelos (solo para que Alembic los vea)
from app.models.inventario import Inventario  # noqa
from app.models.ventas import Venta  # noqa
from app.models.gastos import Gasto  # noqa
from app.models.detalle_venta import DetalleVenta  # noqa

# Base común para todos los modelos
Base = declarative_base()

# 👇 Importar aquí todos los modelos para que Alembic los incluya en Base.metadata
from app.models.inventario import Inventario  # noqa
from app.models.ventas import Venta  # noqa
from app.models.gastos import Gasto  # noqa
from app.models.detalle_venta import DetalleVenta  # noqa
