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
    public,
    enhanced_generator,
    main_generation,
    gpt_test
)
from services.template_service import TemplateService
from ai_services.image_service import image_service

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
app.include_router(html_generator.router, prefix=settings.API_V1_STR, tags=["html-generation"])
app.include_router(presentations.router, prefix=settings.API_V1_STR, tags=["presentations"])
app.include_router(boards.router, prefix=settings.API_V1_STR, tags=["boards"])
app.include_router(templates.router, tags=["templates"])  # Убираем prefix, так как он уже в роутере
app.include_router(preferences.router, prefix=settings.API_V1_STR, tags=["preferences"])
app.include_router(public.router, prefix=settings.API_V1_STR, tags=["public"])
app.include_router(enhanced_generator.router, tags=["enhanced-generation"])
app.include_router(main_generation.router, prefix=settings.API_V1_STR, tags=["main-generation"])
app.include_router(gpt_test.router, prefix=settings.API_V1_STR, tags=["gpt-testing"])


@app.on_event("startup")
async def startup():
    # Создаем таблицы в базе данных
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Инициализируем Redis для rate limiting
    redis_client = redis.from_url(
        settings.REDIS_URL,  # полный URL, включая логин и пароль
        encoding="utf-8",
        decode_responses=True
    )
    await FastAPILimiter.init(redis_client)
    
    print("🚀 База данных и Redis успешно инициализированы!")

    from models.base import get_session
    gen = get_session()
    session = await anext(gen)
    try:
        await TemplateService.create_builtin_templates_in_db(session, user_id=1)
    finally:
        await session.close()

    await image_service._ensure_session()

@app.on_event("shutdown")
async def shutdown_event():
    await image_service.close_session()

@app.get("/")
async def root():
    return {"message": "Welcome to SayDeck API"}

@app.get("/health")
async def health():
    """Простой healthcheck для AWS ECS"""
    return {"status": "ok"}

@app.get("/api/v1/health")
async def api_health():
    """Проверка работоспособности API"""
    return {
        "status": "healthy",
        "message": "SayDeck API v1 - AI Презентации с системой шаблонов",
        "endpoints": {
            "generate_html": "/api/v1/generate/ (POST)",
            "generate_json": "/api/v1/generate/json (POST)",
            "enhanced_generate": "/api/v1/enhanced/generate (POST)",
            "search_images": "/api/v1/enhanced/search-images (GET)",
            "presentations": "/api/v1/presentations",
            "public": "/api/v1/public",
            "templates": "/api/v1/templates",
            "export": "/api/v1/export"
        },
        "features": [
            "Создание HTML презентаций из текста (Groq/OpenAI)",
            "Автоматический поиск и вставка изображений (Pexels API)",
            "Современный дизайн с CSS анимациями", 
            "Автоматическое определение параметров",
            "Сохранение в базу данных",
            "Навигация по слайдам",
            "Умный анализ контента для подбора изображений",
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
            "Enhanced Generator - расширенная генерация с изображениями",
            "Image Service - поиск изображений через Pexels API",
            "Smart Content Analysis - анализ текста для подбора изображений",
            "Template Service - управление публичными шаблонами презентаций"
        ]
    }

print("REDIS URL:", )