# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    username: str
    role: str = "vendedor"       # "admin" o "vendedor"
    is_active: bool = True


class UsuarioCreate(UsuarioBase):
    password: str                # password plano SOLO para crear / cambiar


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UsuarioRead(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
