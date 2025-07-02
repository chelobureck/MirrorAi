"""
AI Services Package - микросервисы для AI провайдеров
"""
from .manager import ai_manager, AIProviderType, AIProviderManager
from .base import AIGenerationRequest, AITranscriptionRequest, AIProvider
from .openai_provider import OpenAIProvider
from .groq_provider import GroqProvider
from .ollama_provider import OllamaProvider

__all__ = [
    "ai_manager",
    "AIProviderType", 
    "AIProviderManager",
    "AIGenerationRequest",
    "AITranscriptionRequest", 
    "AIProvider",
    "OpenAIProvider",
    "GroqProvider", 
    "OllamaProvider"
]
