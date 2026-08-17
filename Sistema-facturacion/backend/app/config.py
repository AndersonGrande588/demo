from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://facturacion_user:facturacion_pass@localhost:5432/facturacion_db"
    SECRET_KEY: str = "hayabuza-facturacion-secret-key-2026-anderson-grande"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()