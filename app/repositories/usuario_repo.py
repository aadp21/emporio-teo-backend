# app/repositories/usuario_repo.py
from typing import Optional

from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.models.usuario import Usuario


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self) -> None:
        super().__init__(Usuario)

    def get_by_email(self, db: Session, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()

    def get_by_username(self, db: Session, username: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.username == username).first()
