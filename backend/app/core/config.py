import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    # DB vars
   import os

DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: str = os.getenv("DB_PORT")
DB_NAME: str = os.getenv("DB_NAME")
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    # База данных
    DATABASE_URL: Optional[str] = None
    
    @property
    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            # Handle neon postgres:// prefix
            if self.DATABASE_URL.startswith("postgres://"):
                return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
            return self.DATABASE_URL
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    # API ключ DeepSeek
    DEEPSEEK_API_KEY: str  # <- обязательная аннотация типа
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173","https://*.devtunnels.ms"]  # обязательно список фронтендов

    # Настройки приложения
    APP_NAME: str = "TTJ Hostel Management"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()
