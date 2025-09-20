"""
Схемы для генерации презентаций по ТЗ
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class PresentationGenerateRequest(BaseModel):
    """Запрос на генерацию презентации"""
    topic: str = Field(..., min_length=1, max_length=500, description="Тема презентации")
    content: Optional[str] = Field(None, max_length=5000, description="Дополнительный текст/контент")
    slides_count: Optional[int] = Field(5, ge=3, le=10, description="Количество слайдов")
    language: str = Field("ru", description="Язык презентации")
    style: Optional[str] = Field("modern", description="Стиль презентации")

class PresentationGenerateResponse(BaseModel):
    """Ответ на генерацию презентации"""
    presentation_id: str = Field(..., description="ID созданной презентации")
    html: str = Field(..., description="Финальный HTML с картинками")
    
class GuestCreditsInfo(BaseModel):
    """Информация о кредитах гостя"""
    session_id: str
    credits: int
    credits_used: int = 0

class ErrorResponse(BaseModel):
    """Стандартный формат ошибки"""
    error: str = Field(..., description="Описание ошибки")
