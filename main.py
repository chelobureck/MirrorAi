from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from config.settings import get_settings
from models.base import Base, engine, init_db
from routers import (
    auth, 
    presentations,
    boards,
    templates,
    preferences,
    public,
)
import os

settings = get_settings()
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production лучше указать конкретные домены
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(presentations.router, prefix=settings.API_V1_STR, tags=["presentations"])
app.include_router(boards.router, prefix=settings.API_V1_STR, tags=["boards"])
app.include_router(templates.router, tags=["templates"])  # Убираем prefix, так как он уже в роутере
app.include_router(preferences.router, prefix=settings.API_V1_STR, tags=["preferences"])
app.include_router(public.router, prefix=settings.API_V1_STR, tags=["public"])

@app.on_event("startup")
async def startup():
    try:
        # Инициализируем базу данных
        await init_db()
        print("✅ База данных успешно инициализирована!")
        
        # Инициализируем Redis для rate limiting
        # В Docker используем правильный URL для Redis
        redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
        print(f"🔗 Подключение к Redis: {redis_url}")
        
        try:
            redis_client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            await FastAPILimiter.init(redis_client)
            print("✅ Redis успешно инициализирован!")
        except Exception as re:
            print(f"⚠️ Redis недоступен или не инициализирован: {re}")
            print("Продолжаем работу без ограничения частоты запросов")
    except Exception as e:
        print(f"❌ Ошибка при запуске приложения: {e}")
        # В production здесь можно добавить логирование и метрики
        raise

@app.get("/")
async def root():
    return {"message": "Welcome to SayDeck API"}

@app.get("/health")
async def health():
    """Простой healthcheck для AWS ECS"""
    return {"status": "healthy"}

@app.get("/api/v1/health")
async def api_health():
    """Проверка работоспособности API"""
    return {
        "status": "healthy",
        "message": "SayDeck API v1 - AI Презентации с системой шаблонов",
        "endpoints": {
            "presentations": "/api/v1/presentations",
            "public": "/api/v1/public",
            "templates": "/api/v1/templates",
            "export": "/api/v1/export"
        },
        "features": [
            "Автоматическое определение параметров",
            "Сохранение в базу данных",
            "Система публичных шаблонов презентаций"
        ],
        "template_system": {
            "save_template": "/api/v1/templates/{presentation_id}/save (POST)",
            "delete_template": "/api/v1/templates/{template_id} (DELETE)",
            "get_template": "/api/v1/templates/{template_id} (GET)",
            "template_viewer": "/api/v1/templates/{template_id}/viewer (GET)",
            "list_templates": "/api/v1/templates (GET)"
        },
        "new_services": [
            "Template Service - управление публичными шаблонами презентаций"
        ]
    }