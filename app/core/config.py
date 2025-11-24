# app/core/config.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = "cambia_esta_clave_super_secreta"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    PROJECT_NAME: str = "Emporio Teo"
    # La dejamos opcional para que Pydantic no lance ValidationError
    DATABASE_URL: str | None = None

    # Configuración correcta para pydantic-settings v2
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

# Fallback por si no se leyó desde .env ni desde variables de entorno
if not settings.DATABASE_URL:
    settings.DATABASE_URL = os.getenv(
        "DATABASE_URL",
        # 👇 Ajusta usuario/clave/nombre BD a tu entorno local
        "postgresql+psycopg2://postgres:Teo2025!@localhost:5432/emporio_teo",
    )


