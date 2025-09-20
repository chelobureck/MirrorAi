from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config.settings import get_settings
import ssl
import os
import urllib.parse
from typing import Optional

settings = get_settings()


def _build_database_url() -> str:
    """Строит правильный URL для подключения к базе данных.
    Приоритеты:
    1) DATABASE_URL (полный DSN)
    2) POSTGRES_SERVER как полный DSN
    3) Сборка из компонент (USER/PASSWORD/SERVER/PORT/DB)
    """
    if settings.USE_POSTGRES.lower() == "true":
        # 1) Прямой DSN через DATABASE_URL
        db_url_env = os.getenv("DATABASE_URL") or settings.DATABASE_URL
        if db_url_env:
            dsn = db_url_env
            # Убираем sslmode/ssl из URL, т.к. SSL управляется через connect_args
            if "?" in dsn:
                base, _, _ = dsn.partition("?")
                dsn = base
            return dsn

        # 2) POSTGRES_SERVER задан как полный DSN
        server_val = settings.POSTGRES_SERVER or ""
        if "://" in server_val:
            dsn = server_val
            # Если в DSN встречается placeholder ':password@', подставим реальный пароль
            if ":password@" in dsn and settings.POSTGRES_PASSWORD:
                dsn = dsn.replace(
                    ":password@",
                    f":{urllib.parse.quote_plus(settings.POSTGRES_PASSWORD)}@"
                )
            # Убираем sslmode из URL, так как он будет передан через connect_args
            if "?sslmode=" in dsn:
                dsn = dsn.split("?")[0]
            return dsn

        # 3) Сборка из компонент (без sslmode в URL)
        safe_password = urllib.parse.quote_plus(settings.POSTGRES_PASSWORD)
        base_url = (
            f"postgresql+asyncpg://{settings.POSTGRES_USER}:{safe_password}"
            f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )
        return base_url
    else:
        return "sqlite+aiosqlite:///./saydeck.db"


# Создаем движок с правильными настройками
database_url = _build_database_url()

if "sqlite" in database_url:
    # Для SQLite используем простые настройки
    engine = create_async_engine(
        database_url,
        echo=True,
        pool_pre_ping=True
    )
else:
    # Для PostgreSQL используем расширенные настройки
    # SSL настройки передаем через connect_args, а не через URL
    is_production = (os.getenv("ENVIRONMENT") or settings.ENVIRONMENT) == "production"
    
    connect_args = {
        "server_settings": {
            "application_name": "SayDeck",
            "timezone": "UTC"
        }
    }
    
    # SSL настройки для asyncpg
    # В AWS/production и при явных признаках sslmode=require используем SSLContext
    env_value = os.getenv("ENVIRONMENT") or settings.ENVIRONMENT
    is_aws_or_production = (
        is_production or 
        "aws" in env_value.lower() or 
        "render" in env_value.lower() or
        "production" in env_value.lower()
    )

    sslmode_hint = (os.getenv("DATABASE_URL") or "").lower()
    ssl_required_by_url = ("sslmode=require" in sslmode_hint)
    url_hostport = database_url.split("@")[1] if "@" in database_url else database_url
    host_part = url_hostport.split("/")[0]
    ssl_required_by_host = ("rds.amazonaws.com" in host_part) or ("render.com" in host_part)

    must_use_ssl = is_aws_or_production or ssl_required_by_url or ssl_required_by_host

    if must_use_ssl:
        # Управляем верификацией сертификата через переменную POSTGRES_SSL_VERIFY=true|false (по умолчанию true)
        ssl_verify = (os.getenv("POSTGRES_SSL_VERIFY") or "true").lower() == "true"
        ssl_ctx = ssl.create_default_context()
        if not ssl_verify:
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE
            print(f"🔒 SSL: insecure context (verify=FALSE) для окружения: {env_value}")
        else:
            print(f"🔒 SSL: verified context (verify=TRUE) для окружения: {env_value}")
        connect_args["ssl"] = ssl_ctx
    else:
        # Для локальной разработки можно отключить SSL
        connect_args["ssl"] = False
        print(f"🔓 SSL отключен для окружения: {env_value}")
    
    engine = create_async_engine(
        database_url,
        echo=True,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=30,
        pool_recycle=3600,
        connect_args=connect_args
    )

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_session():
    """Получает сессию базы данных с обработкой ошибок"""
    try:
        async with async_session() as session:
            yield session
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        raise


async def init_db():
    """Инициализирует базу данных"""
    try:
        print(f"🔌 Попытка подключения к БД: {database_url.split('@')[1] if '@' in database_url else database_url}")
        print(f"🔒 SSL настройки: {connect_args.get('ssl', 'не указано')}")
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ База данных успешно инициализирована")
    except Exception as e:
        print(f"❌ Ошибка инициализации базы данных: {e}")
        print(f"🔍 Тип ошибки: {type(e).__name__}")
        if "SSL" in str(e):
            print("💡 Подсказка: Проверьте настройки SSL и переменную ENVIRONMENT")
        raise 