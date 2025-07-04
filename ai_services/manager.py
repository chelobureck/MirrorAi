"""
AI Provider Manager - управляет всеми AI провайдерами
"""
from typing import Dict, List, Optional
from enum import Enum
from .base import AIProvider, AIGenerationRequest
from .groq_provider import GroqProvider

class AIProviderType(Enum):
    """Типы AI провайдеров"""
    GROQ = "groq"

class AIProviderManager:
    """Менеджер для управления AI провайдерами - только Groq"""
    
    def __init__(self):
        self.providers: Dict[AIProviderType, AIProvider] = {
            AIProviderType.GROQ: GroqProvider(),
        }
        self.default_provider = AIProviderType.GROQ  # Только Groq
    
    def get_provider(self, provider_type: Optional[AIProviderType] = None) -> AIProvider:
        """Получает провайдера по типу"""
        if provider_type is None:
            provider_type = self.default_provider
        
        provider = self.providers.get(provider_type)
        if not provider:
            raise ValueError(f"Provider {provider_type} not found")
        
        return provider
    
    def get_available_providers(self) -> List[Dict]:
        """Возвращает список доступных провайдеров"""
        available = []
        for provider_type, provider in self.providers.items():
            available.append({
                "type": provider_type.value,
                "name": provider.get_provider_name(),
                "available": provider.is_available(),
                "is_default": provider_type == self.default_provider
            })
        return available
    
    def get_best_available_provider(self) -> AIProvider:
        """Возвращает Groq провайдер"""
        return self.providers[AIProviderType.GROQ]
    
    async def generate_presentation(
        self, 
        request: AIGenerationRequest, 
        provider_type: Optional[AIProviderType] = None
    ) -> Dict:
        """Генерирует презентацию через указанный или лучший провайдер"""
        if provider_type:
            provider = self.get_provider(provider_type)
        else:
            provider = self.get_best_available_provider()
        
        result = await provider.generate_presentation(request)
        
        # Добавляем метаданные о провайдере
        result["_metadata"] = {
            "provider": provider.get_provider_name(),
            "provider_type": provider_type.value if provider_type else "auto",
            "generated_by": "SayDeck AI Services"
        }
        
        return result

# Глобальный экземпляр менеджера
ai_manager = AIProviderManager()
