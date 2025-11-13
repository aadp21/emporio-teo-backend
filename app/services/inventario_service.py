# app/services/inventario_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.inventario_repo import InventarioRepository
from app.schemas.inventario import InventarioCreate, InventarioUpdate

class InventarioService:
    def __init__(self):
        self.repo = InventarioRepository()

    def crear_producto(self, db: Session, obj_in: InventarioCreate):
        # validar código duplicado
        existing = self.repo.get_by_codigo(db, obj_in.codigo)
        if existing:
            # si existe, sumamos cantidad como hacías tú
            updated = self.repo.update(
                db,
                existing,
                {"cantidad": existing.cantidad + obj_in.cantidad}
            )
            return updated
        return self.repo.create(db, obj_in.model_dump())

    def listar(self, db: Session, skip=0, limit=100):
        return self.repo.get_multi(db, skip=skip, limit=limit)

    def actualizar(self, db: Session, id: int, obj_in: InventarioUpdate):
        producto = self.repo.get(db, id)
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return self.repo.update(db, producto, obj_in.model_dump(exclude_unset=True))
