from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from config.settings import get_settings
from models.base import Base, engine
from routers import (
    auth, 
    presentations, 
    generate_v2, 
    public, 
    export, 
    boards, 
    templates, 
    preferences
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
app.include_router(presentations.router, prefix=settings.API_V1_STR, tags=["presentations"])
app.include_router(generate_v2.router, prefix=settings.API_V1_STR, tags=["generate"])
app.include_router(public.router, prefix=settings.API_V1_STR, tags=["public"])
app.include_router(export.router, prefix=settings.API_V1_STR, tags=["export"])
app.include_router(boards.router, prefix=settings.API_V1_STR, tags=["boards"])
app.include_router(templates.router, prefix=settings.API_V1_STR, tags=["templates"])
app.include_router(preferences.router, prefix=settings.API_V1_STR, tags=["user-preferences"])


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
        "message": "SayDeck API v1 работает",
        "endpoints": {
            "generate": "/api/v1/generate/providers",
            "presentations": "/api/v1/presentations",
            "public": "/api/v1/public",
            "export": "/api/v1/export"
        }
    }