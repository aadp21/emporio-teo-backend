# app/services/usuario_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.usuario_repo import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash, verify_password


class UsuarioService:
    def __init__(self) -> None:
        self.repo = UsuarioRepository()

    def crear_usuario(self, db: Session, obj_in: UsuarioCreate):
        # ¿ya existe por email?
        if self.repo.get_by_email(db, obj_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con ese email",
            )

        # ¿ya existe por username?
        if self.repo.get_by_username(db, obj_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con ese nombre de usuario",
            )

        data = obj_in.model_dump()
        password_plano = data.pop("password")
        data["hashed_password"] = get_password_hash(password_plano)

        return self.repo.create(db, data)

    def actualizar_usuario(self, db: Session, user_id: int, obj_in: UsuarioUpdate):
        usuario = self.repo.get(db, user_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        data = obj_in.model_dump(exclude_unset=True)

        if "password" in data:
            password_plano = data.pop("password")
            data["hashed_password"] = get_password_hash(password_plano)

        return self.repo.update(db, usuario, data)

    def autenticar(self, db: Session, username: str, password: str):
        """
        Autentica por username + password.
        Devuelve el usuario si es válido, o None si no.
        """
        usuario = self.repo.get_by_username(db, username)
        if not usuario:
            return None
        if not verify_password(password, usuario.hashed_password):
            return None
        return usuario
