from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config.settings import get_settings
import ssl
import os

settings = get_settings()

# Настройка соединения в зависимости от типа базы данных
if "sqlite" in settings.DATABASE_URL:
    # Для SQLite не нужны SSL настройки
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True
    )
else:
    # Для PostgreSQL в Docker - без SSL
    clean_url = settings.DATABASE_URL.replace("?sslmode=disable", "")
    engine = create_async_engine(
        clean_url,
        echo=True
    )

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_session():
    async with async_session() as session:
        yield session 