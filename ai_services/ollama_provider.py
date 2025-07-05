"""
Ollama Provider - локальные Llama модели
"""
import json
import httpx
from typing import Dict, Any
from config.settings import get_settings
from .base import AIProvider, AIGenerationRequest

settings = get_settings()

class OllamaProvider(AIProvider):
    """Провайдер для локальных Llama моделей через Ollama"""
    
    def __init__(self):
        # Настройки для Ollama
        self.base_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = getattr(settings, 'OLLAMA_MODEL', 'llama3.1:8b')
        self.timeout = 120  # Увеличенный таймаут для локальных моделей
    
    async def generate_presentation(self, request: AIGenerationRequest) -> Dict[str, Any]:
        """Генерирует презентацию через локальную Llama"""
        if not await self.is_available():
            raise ValueError("Ollama service is not available")
        
        prompt = f"""
        Создай структуру презентации на языке: {request.language}. 
        Количество слайдов: {request.slides_count}
        
        Верни ТОЛЬКО валидный JSON с полями:
        - title: заголовок презентации
        - slides: массив слайдов, где каждый слайд имеет поля:
            - title: заголовок слайда в HTML формате
            - content: основной текст слайда в HTML формате
            - type: тип слайда (title, content, image)
        
        ОБЯЗАТЕЛЬНО используй HTML теги для форматирования:
        - <h1>, <h2>, <h3> для заголовков
        - <p> для абзацев
        - <strong> для важного текста
        - <em> для выделения
        - <ul>, <li> для списков
        - <br> для переносов
        
        Пример:
        {{
            "title": "Заголовок презентации",
            "slides": [
                {{
                    "title": "<h1>Заголовок слайда</h1>",
                    "content": "<p>Текст с <strong>выделением</strong></p><ul><li>Пункт 1</li></ul>",
                    "type": "title"
                }}
            ]
        }}
        
        Текст: {request.text}
        
        Ответ должен быть только JSON, без дополнительного текста.
        """
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9
                        }
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result.get("response", "").strip()
                    
                    # Очищаем от возможных markdown блоков
                    if content.startswith("```json"):
                        content = content[7:]
                    if content.endswith("```"):
                        content = content[:-3]
                    
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        return self._create_fallback_presentation(request)
                else:
                    return self._create_fallback_presentation(request)
                    
        except Exception as e:
            print(f"Ollama generation error: {e}")
            return self._create_fallback_presentation(request)
    
    def get_provider_name(self) -> str:
        return f"Ollama ({self.model})"
    
    async def is_available(self) -> bool:
        """Проверяет доступность Ollama сервиса"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False
    
    def is_available(self) -> bool:
        """Синхронная версия для совместимости"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.is_available_async())
        except:
            return False
    
    def _create_fallback_presentation(self, request: AIGenerationRequest) -> Dict[str, Any]:
        """Создает fallback презентацию"""
        return {
            "title": f"Локальная презентация: {request.text[:30]}...",
            "slides": [
                {
                    "title": "Заголовок презентации",
                    "content": "Эта презентация создана с помощью локальной Llama модели",
                    "type": "title"
                },
                {
                    "title": f"Анализ контента",
                    "content": f"Основной текст для анализа: {request.text[:300]}...",
                    "type": "content"
                },
                {
                    "title": "Выводы",
                    "content": "Локальная обработка данных обеспечивает приватность и контроль",
                    "type": "content"
                }
            ]
        }
