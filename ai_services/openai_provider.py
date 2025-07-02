"""
OpenAI Provider - существующий провайдер
"""
import openai
import json
from typing import Dict, Any
from config.settings import get_settings
from .base import AIProvider, AIGenerationRequest, AITranscriptionRequest

settings = get_settings()

class OpenAIProvider(AIProvider):
    """Провайдер OpenAI"""
    
    def __init__(self):
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_key":
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.client = None
    
    async def generate_presentation(self, request: AIGenerationRequest) -> Dict[str, Any]:
        """Генерирует презентацию через OpenAI GPT-4"""
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        prompt = f"""
        Создай структуру презентации на языке: {request.language}. 
        Количество слайдов: {request.slides_count}
        Анимация: {"включена" if request.animation else "отключена"}
        
        Верни ТОЛЬКО валидный JSON с полями:
        - title: заголовок презентации
        - slides: массив слайдов, где каждый слайд имеет поля:
            - title: заголовок слайда
            - content: основной текст слайда
            - type: тип слайда (title, content, image, etc.)
        
        Текст: {request.text}
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты - эксперт по созданию презентаций. Отвечай только валидным JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return self._create_fallback_presentation(request)
    
    async def transcribe_audio(self, request: AITranscriptionRequest) -> str:
        """Транскрибирует аудио через Whisper"""
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        with open(request.audio_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    
    def get_provider_name(self) -> str:
        return "OpenAI"
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def _create_fallback_presentation(self, request: AIGenerationRequest) -> Dict[str, Any]:
        """Создает fallback презентацию если JSON parsing не удался"""
        return {
            "title": "Сгенерированная презентация",
            "slides": [
                {
                    "title": f"Слайд {i+1}",
                    "content": f"Содержимое слайда {i+1}",
                    "type": "content"
                } for i in range(request.slides_count)
            ]
        }
