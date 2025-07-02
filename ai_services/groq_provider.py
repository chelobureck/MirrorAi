"""
Groq Provider - новый высокоскоростной провайдер
"""
import json
from typing import Dict, Any
from groq import Groq
from config.settings import get_settings
from .base import AIProvider, AIGenerationRequest, AITranscriptionRequest

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
            raise ValueError("Groq API key not configured")
        
        # Улучшенный промпт для Groq Llama
        prompt = f"""
        Создай профессиональную презентацию на {request.language} языке.
        
        ПАРАМЕТРЫ:
        - Количество слайдов: {request.slides_count}
        - Исходный текст: {request.text}
        - Анимация: {"включена" if request.animation else "отключена"}
        
        ТРЕБОВАНИЯ:
        1. Верни ТОЛЬКО валидный JSON без markdown блоков
        2. Создай логичную структуру от введения к заключению
        3. Каждый слайд должен быть информативным и не превышать 150 слов
        4. Используй профессиональный деловой тон
        
        ФОРМАТ JSON:
        {{
            "title": "Заголовок презентации",
            "slides": [
                {{
                    "title": "Заголовок слайда",
                    "content": "Основной текст слайда",
                    "type": "title|content|conclusion"
                }}
            ]
        }}
        
        Проанализируй исходный текст и создай структурированную презентацию с четкой логикой изложения.
        """
        
        try:
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",  # Самая мощная модель Groq
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
            
            # Очищаем от возможных markdown блоков и лишних символов
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            content = content.strip()
            
            # Парсим JSON
            result = json.loads(content)
            
            # Валидируем структуру
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
    
    async def transcribe_audio(self, request: AITranscriptionRequest) -> str:
        """Groq пока не поддерживает транскрипцию, используем fallback"""
        # Groq не поддерживает Whisper, возвращаем заглушку
        return f"[Транскрипция через Groq пока недоступна для файла: {request.audio_file_path}]"
    
    def get_provider_name(self) -> str:
        return "Groq (Llama 3.1)"
    
    def is_available(self) -> bool:
        """Проверяет доступность Groq API"""
        client = self._ensure_client()
        return client is not None
    
    def _create_fallback_presentation(self, request: AIGenerationRequest) -> Dict[str, Any]:
        """Создает fallback презентацию"""
        return {
            "title": f"Презентация на тему: {request.text[:50]}...",
            "slides": [
                {
                    "title": "Введение",
                    "content": "Добро пожаловать в презентацию, созданную с помощью Groq AI",
                    "type": "title"
                },
                {
                    "title": f"Основная тема",
                    "content": f"Анализ текста: {request.text[:200]}...",
                    "type": "content"
                },
                {
                    "title": "Заключение",
                    "content": "Спасибо за внимание!",
                    "type": "conclusion"
                }
            ]
        }
