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
        self.client = None
        self._initialized = False
    
    def _ensure_client(self):
        """Ленивая инициализация OpenAI клиента"""
        if not self._initialized:
            openai_key = getattr(settings, 'OPENAI_API_KEY', None)
            if openai_key and openai_key != "your_openai_key":
                self.client = openai.OpenAI(api_key=openai_key)
                print(f"✓ OpenAI initialized with key: {openai_key[:10]}...")
            else:
                self.client = None
                print("❌ OpenAI API key not configured properly")
            self._initialized = True
        return self.client
    
    async def generate_presentation(self, request: AIGenerationRequest) -> Dict[str, Any]:
        """Генерирует презентацию через OpenAI GPT-4"""
        client = self._ensure_client()
        if not client:
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
        
        response = client.chat.completions.create(
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
        client = self._ensure_client()
        if not client:
            raise ValueError("OpenAI API key not configured")
        
        with open(request.audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    
    def get_provider_name(self) -> str:
        return "OpenAI"
    
    def is_available(self) -> bool:
        client = self._ensure_client()
        return client is not None
    
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
