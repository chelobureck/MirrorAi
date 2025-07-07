"""
Groq Provider - новый высокоскоростной провайдер
"""
import json
from typing import Dict, Any
from groq import Groq
from config.settings import get_settings
from .base import AIProvider, AIGenerationRequest

settings = get_settings()

class GroqProvider(AIProvider):
    """Провайдер Groq - быстрые LLM модели"""

    def __init__(self):
        self.client = None
        self._initialized = False

    def _ensure_client(self):
        """Ленивая инициализация Groq клиента"""
        if not self._initialized:
            groq_key = getattr(settings, 'GROQ_API_KEY', None)
            if groq_key and groq_key != "your_groq_key" and groq_key.startswith('gsk_'):
                self.client = Groq(api_key=groq_key)
                print(f"✓ Groq initialized with key: {groq_key[:10]}...")
            else:
                self.client = None
                print("❌ Groq API key not configured properly")
            self._initialized = True
        return self.client

    async def generate_presentation(self, request: AIGenerationRequest) -> Dict[str, Any]:
        """Генерирует презентацию через Groq Llama"""
        client = self._ensure_client()
        if not client:
            print("🚀 Using demo mode - no Groq API key configured")
            return self._generate_demo_presentation(request)

        try:
            return await self._generate_real_presentation(request, client)
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            print("🚀 Falling back to demo mode")
            return self._generate_demo_presentation(request)

    async def _generate_real_presentation(self, request: AIGenerationRequest, client) -> Dict[str, Any]:
        """Генерирует презентацию через реальный Groq API"""
        topic = request.topic or "Презентация"
        content = request.content or ""

        prompt = f"""Создай профессиональную презентацию на тему "{topic}" на {request.language} языке.

Дополнительная информация: {content}
Количество слайдов: {request.slides_count}

ТРЕБОВАНИЯ:
1. Верни ТОЛЬКО валидный JSON без markdown блоков
2. Структура: титульный слайд → контентные слайды → заключение
3. Каждый слайд: заголовок + содержательный текст (50-150 слов)
4. Используй HTML теги для форматирования: <h2>, <p>, <strong>, <ul>, <li>

JSON формат:
{{
    "title": "{topic}",
    "slides": [
        {{
            "title": "Заголовок слайда",
            "content": "<p>Содержание с <strong>акцентами</strong></p>",
            "type": "title"
        }}
    ]
}}

ИСХОДНЫЙ ТЕКСТ ДЛЯ АНАЛИЗА: {request.text or 'Нет дополнительного текста'}
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты эксперт по созданию презентаций. Отвечай ТОЛЬКО валидным JSON без дополнительных комментариев и markdown блоков."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                top_p=1,
                stream=False
            )

            content = response.choices[0].message.content.strip()

            # Очищаем от markdown блоков
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]

            content = content.strip()
            result = json.loads(content)

            if not isinstance(result, dict) or 'title' not in result or 'slides' not in result:
                raise ValueError("Invalid response structure")

            print(f"✓ Groq successfully generated presentation: {result['title']}")
            return result

        except json.JSONDecodeError as e:
            print(f"❌ Groq JSON parsing error: {e}")
            print(f"Raw response: {content[:200]}...")
            return self._create_fallback_presentation(request)
        except Exception as e:
            print(f"❌ Groq generation error: {e}")
            return self._create_fallback_presentation(request)

    def get_provider_name(self) -> str:
        return "Groq (Llama 3.1)"

    def is_available(self) -> bool:
        client = self._ensure_client()
        return client is not None

    def _create_fallback_presentation(self, request: AIGenerationRequest) -> Dict[str, Any]:
        return {
            "title": f"Презентация на тему: {request.topic or request.text[:50] if request.text else 'Неизвестная тема'}...",
            "slides": [
                {
                    "title": "Введение",
                    "content": "<p>Добро пожаловать в презентацию, созданную с помощью <strong>Groq AI</strong></p>",
                    "type": "title"
                },
                {
                    "title": f"Основная тема",
                    "content": f"<p>Анализ темы: <strong>{request.topic or 'Неизвестная тема'}</strong></p><p>{request.content or request.text[:200] if request.text else 'Здесь будет детальная информация по теме.'}...</p>",
                    "type": "content"
                },
                {
                    "title": "Заключение",
                    "content": "<p>Спасибо за внимание!</p><p><em>Презентация создана системой SayDeck</em></p>",
                    "type": "conclusion"
                }
            ]
        }

    def _generate_demo_presentation(self, request: AIGenerationRequest) -> Dict[str, Any]:
        slides = [
            {
                "title": request.topic or "Демо презентация",
                "content": "<p>Презентация создана системой <strong>SayDeck</strong> в демо-режиме</p>",
                "type": "title"
            }
        ]

        for i in range(request.slides_count - 1):
            slide_num = i + 2
            slides.append({
                "title": f"Раздел {slide_num}",
                "content": f"<p>Содержимое раздела <strong>{slide_num}</strong> по теме '<em>{request.topic or 'Демо тема'}</em>'.</p><p>{request.content or 'Здесь будет детальная информация по теме.'}</p>",
                "type": "content"
            })

        return {
            "title": request.topic or "Демо презентация",
            "slides": slides,
            "metadata": {
                "provider": "Groq Demo",
                "generated_at": "2025-07-06",
                "mode": "demo"
            }
        }
