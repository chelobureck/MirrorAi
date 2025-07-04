from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from config.settings import get_settings
from models.base import Base, engine
from routers import (
    auth, 
    html_generator,
    presentations,
    boards,
    templates,
    preferences,
    public
)

settings = get_settings()
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(html_generator.router, prefix=settings.API_V1_STR, tags=["html-generation"])
app.include_router(presentations.router, prefix=settings.API_V1_STR, tags=["presentations"])
app.include_router(boards.router, prefix=settings.API_V1_STR, tags=["boards"])
app.include_router(templates.router, prefix=settings.API_V1_STR, tags=["templates"])
app.include_router(preferences.router, prefix=settings.API_V1_STR, tags=["preferences"])
app.include_router(public.router, prefix=settings.API_V1_STR, tags=["public"])


@app.on_event("startup")
async def startup():
    # Создаем таблицы в базе данных
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Инициализируем Redis для rate limiting
    redis_client = redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True
    )
    await FastAPILimiter.init(redis_client)
    
    print("🚀 База данных и Redis успешно инициализированы!")

@app.get("/")
async def root():
    return {"message": "Welcome to SayDeck API"}

@app.get("/api/v1/health")
async def api_health():
    """Проверка работоспособности API"""
    return {
        "status": "healthy",
        "message": "SayDeck API v1 - Groq HTML Презентации",
        "endpoints": {
            "generate_html": "/api/v1/generate/ (POST)",
            "generate_json": "/api/v1/generate/json (POST)",
            "presentations": "/api/v1/presentations",
            "public": "/api/v1/public",
            "export": "/api/v1/export"
        },
        "features": [
            "Создание HTML презентаций из текста (только Groq)",
            "Современный дизайн с CSS анимациями", 
            "Автоматическое определение параметров",
            "Сохранение в базу данных",
            "Навигация по слайдам"
        ]
    }