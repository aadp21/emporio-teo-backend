from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.services.usuario_service import UsuarioService
from app.schemas.usuario import UsuarioCreate, UsuarioRead
from app.core.deps import get_current_admin_user, get_current_active_user

router = APIRouter()
service = UsuarioService()


@router.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Login por username + password.
    Devuelve un token JWT tipo Bearer.
    """
    usuario = service.autenticar(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o contraseña incorrectos",
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": usuario.username, "role": usuario.role},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post(
    "/auth/usuarios",
    response_model=UsuarioRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_usuario(
    usuario_in: UsuarioCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin_user),
):
    """
    Crear usuario nuevo.
    Solo permitido para usuarios con rol 'admin'.
    """
    return service.crear_usuario(db, usuario_in)


@router.get("/auth/me", response_model=UsuarioRead)
def leer_usuario_actual(
    current_user=Depends(get_current_active_user),
):
    """
    Devuelve el usuario actual (a partir del token).
    """
    return current_user
