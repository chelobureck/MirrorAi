from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str

    # CORS
    BACKEND_CORS_ORIGINS: List[str]

    # Безопасность
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # База данных
    USE_POSTGRES: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    DATABASE_URL: str | None = None

    # Redis
    REDIS_URL: str

    # OpenAI / Groq
    OPENAI_API_KEY: str
    GROQ_API_KEY: str

    # Pexels
    PEXELS_API_KEY: str

    # Ollama
    OLLAMA_BASE_URL: str
    OLLAMA_MODEL: str

    # Микросервис изображений
    IMAGE_MICROSERVICE_URL: str
    IMAGE_MICROSERVICE_TIMEOUT: int

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # Gmail SMTP
    GMAIL_USER: str
    GMAIL_APP_PASSWORD: str

    # Окружение
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
