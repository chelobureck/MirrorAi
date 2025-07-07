"""
Базовый интерфейс для AI провайдеров
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class AIGenerationRequest(BaseModel):
    """Запрос для генерации презентации"""
    text: str
    topic: Optional[str] = None
    content: Optional[str] = None  
    language: str = "ru"
    slides_count: int = 5
    animation: bool = False
    template: Optional[str] = None

class AIProvider(ABC):
    """Базовый класс для AI провайдеров"""
    
    @abstractmethod
    async def generate_presentation(self, request: AIGenerationRequest) -> Dict[str, Any]:
        """Генерирует структуру презентации"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Возвращает название провайдера"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Проверяет доступность провайдера"""
        pass
