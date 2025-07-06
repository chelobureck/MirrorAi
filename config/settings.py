from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = "SayDeck"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Переключатель базы данных (для Docker/локальной разработки)
    USE_POSTGRES: str = "false"
    
    # Настройки безопасности
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Настройки базы данных
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    
    # Настройки Redis для rate limiting
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    
    # Настройки OpenAI
    OPENAI_API_KEY: str
    
    # Настройки Groq
    GROQ_API_KEY: str = "your_groq_key"
    
    # Настройки Pexels API для поиска изображений
    PEXELS_API_KEY: str = "your_pexels_api_key"
    
    # Настройки Ollama (локальная Llama)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"
    
    # Настройки микросервиса изображений
    IMAGE_MICROSERVICE_URL: str = "http://image-service:8080"
    IMAGE_MICROSERVICE_TIMEOUT: int = 30
    
    # Настройки Google OAuth
    GOOGLE_CLIENT_ID: str = "your_google_client_id"
    GOOGLE_CLIENT_SECRET: str = "your_google_client_secret"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google-callback"
    
    # Настройки Gmail для отправки писем
    GMAIL_USER: str
    GMAIL_APP_PASSWORD: str
    
    @property
    def DATABASE_URL(self) -> str:
        # Для локальной разработки используем SQLite
        import os
        if self.USE_POSTGRES.lower() == "true":
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}?sslmode=disable"
        else:
            return "sqlite+aiosqlite:///./saydeck.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()