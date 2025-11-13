# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Emporio Teo"
    DATABASE_URL: str  # sin valor por defecto, que venga del entorno

    class Config:
        env_file = ".env"

settings = Settings()