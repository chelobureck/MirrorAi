from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional

class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = "MirrorAI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

    # Безопасность
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # База данных
    USE_POSTGRES: str = "False"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "mirrorai"
    DATABASE_URL: Optional[str] = None

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # OpenAI / Groq
    OPENAI_API_KEY: str = "your-openai-key"
    GROQ_API_KEY: str = "your-groq-key"

    # Pexels
    PEXELS_API_KEY: str = "your-pexels-key"

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "default-model"

    # Микросервис изображений
    IMAGE_MICROSERVICE_URL: str = "http://localhost:8001"
    IMAGE_MICROSERVICE_TIMEOUT: int = 10

    # Google OAuth
    GOOGLE_CLIENT_ID: str = "your-google-client-id"
    GOOGLE_CLIENT_SECRET: str = "your-google-client-secret"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    # Gmail SMTP
    GMAIL_USER: str = "your-gmail-user"
    GMAIL_APP_PASSWORD: str = "your-gmail-app-password"

    # Окружение
    ENVIRONMENT: str = "development"

    # Добавьте все "лишние" переменные из .env:
    APP_HOST: Optional[str] = None
    APP_PORT: Optional[str] = None
    APP_DEBUG: Optional[str] = None
    APP_CORS_ORIGINS: Optional[str] = None
    JWT_SECRET: Optional[str] = None
    JWT_ALG: Optional[str] = None
    FIREBASE_PROJECT_ID: Optional[str] = None
    FIREBASE_ENABLED: Optional[str] = None

    # --- ДОБАВЛЕНЫ недостающие переменные из .env ---
    OPENAI_BASE_URL: Optional[str] = None
    OPENAI_MODEL: Optional[str] = None
    OPENAI_TIMEOUT: Optional[str] = None

    DB_HOST: Optional[str] = None
    DB_PORT: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None

    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[str] = None
    REDIS_DB: Optional[str] = None
    REDIS_TTL_SECONDS: Optional[str] = None

    GOOGLE_REFRESH_TOKEN: Optional[str] = None

    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[str] = None
    SMTP_USER: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
