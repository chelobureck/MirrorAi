"""
AI Provider Manager - управляет всеми AI провайдерами
"""
from typing import Dict, List, Optional
from enum import Enum
from .base import AIProvider, AIGenerationRequest, AITranscriptionRequest
from .openai_provider import OpenAIProvider
from .groq_provider import GroqProvider
from .ollama_provider import OllamaProvider

class AIProviderType(Enum):
    """Типы AI провайдеров"""
    OPENAI = "openai"
    GROQ = "groq"
    OLLAMA = "ollama"

class AIProviderManager:
    """Менеджер для управления AI провайдерами"""
    
    def __init__(self):
        self.providers: Dict[AIProviderType, AIProvider] = {
            AIProviderType.OPENAI: OpenAIProvider(),
            AIProviderType.GROQ: GroqProvider(),
            AIProviderType.OLLAMA: OllamaProvider(),
        }
        self.default_provider = AIProviderType.GROQ  # Groq как основной
    
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
        """Возвращает лучший доступный провайдер"""
        # Приоритет: Groq > OpenAI > Ollama
        priority_order = [AIProviderType.GROQ, AIProviderType.OPENAI, AIProviderType.OLLAMA]
        
        for provider_type in priority_order:
            provider = self.providers[provider_type]
            if provider.is_available():
                return provider
        
        # Если ни один не доступен, возвращаем первый (с fallback)
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
    
    async def transcribe_audio(
        self, 
        request: AITranscriptionRequest, 
        provider_type: Optional[AIProviderType] = None
    ) -> str:
        """Транскрибирует аудио через указанный или лучший провайдер"""
        if provider_type:
            provider = self.get_provider(provider_type)
        else:
            # Для транскрипции предпочитаем OpenAI (Whisper)
            if self.providers[AIProviderType.OPENAI].is_available():
                provider = self.providers[AIProviderType.OPENAI]
            else:
                provider = self.get_best_available_provider()
        
        return await provider.transcribe_audio(request)

# Глобальный экземпляр менеджера
ai_manager = AIProviderManager()
