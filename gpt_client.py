"""
GPT Client для работы с OpenAI API
Модуль для централизованного управления запросами к GPT API
"""

import os
import asyncio
from typing import Optional, Dict, Any, List
from openai import AsyncOpenAI
import httpx
from config.settings import get_settings

settings = get_settings()

class GPTClient:
    """Клиент для работы с OpenAI GPT API"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.timeout = 30  # Таймаут в секундах
        self.max_retries = 3
        
    async def get_gpt_response(
        self, 
        prompt: str, 
        model: str = "gpt-4o-mini",
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Отправляет запрос к GPT API и возвращает ответ
        
        Args:
            prompt: Пользовательский промпт
            model: Модель GPT для использования
            max_tokens: Максимальное количество токенов в ответе
            temperature: Температура генерации (0.0 - 1.0)
            system_prompt: Системный промпт (опционально)
        
        Returns:
            str: Ответ от GPT API
        
        Raises:
            Exception: При ошибках API или таймауте
        """
        if not self.api_key:
            raise Exception("OpenAI API key not configured")
            
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        messages.append({"role": "user", "content": prompt})
        
        for attempt in range(self.max_retries):
            try:
                response = await asyncio.wait_for(
                    self._make_openai_request(messages, model, max_tokens, temperature),
                    timeout=self.timeout
                )
                    
                return response.choices[0].message.content.strip()
                
            except asyncio.TimeoutError:
                if attempt == self.max_retries - 1:
                    raise Exception(f"GPT API timeout after {self.timeout} seconds")
                await asyncio.sleep(2 ** attempt)  # Экспоненциальная задержка
                
            except Exception as e:
                if "rate limit" in str(e).lower():
                    if attempt == self.max_retries - 1:
                        raise Exception("GPT API rate limit exceeded")
                    await asyncio.sleep(5 * (attempt + 1))  # Увеличиваем задержку
                elif attempt == self.max_retries - 1:
                    raise Exception(f"GPT API error: {str(e)}")
                else:
                    await asyncio.sleep(2 ** attempt)
    
    async def _make_openai_request(
        self, 
        messages: List[Dict[str, str]], 
        model: str, 
        max_tokens: Optional[int], 
        temperature: float
    ):
        """Выполняет запрос к OpenAI API"""
        request_params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            request_params["max_tokens"] = max_tokens
            
        return await self.client.chat.completions.create(**request_params)
    
    async def get_streaming_response(
        self,
        prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ):
        """
        Получает потоковый ответ от GPT API
        
        Args:
            prompt: Пользовательский промпт
            model: Модель GPT для использования
            temperature: Температура генерации
            system_prompt: Системный промпт (опционально)
        
        Yields:
            str: Части ответа по мере генерации
        """
        if not self.api_key:
            raise Exception("OpenAI API key not configured")
            
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=True
            )
            
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise Exception(f"Streaming GPT API error: {str(e)}")

# Создаем глобальный экземпляр клиента
gpt_client = GPTClient()

# Удобные функции для быстрого использования
async def get_gpt_response(prompt: str, **kwargs) -> str:
    """Удобная функция для получения ответа от GPT"""
    return await gpt_client.get_gpt_response(prompt, **kwargs)

async def get_gpt_streaming_response(prompt: str, **kwargs):
    """Удобная функция для получения потокового ответа от GPT"""
    async for chunk in gpt_client.get_streaming_response(prompt, **kwargs):
        yield chunk

# Функции для разных типов задач
async def generate_presentation_content(topic: str, num_slides: int = 5) -> str:
    """Генерирует контент для презентации"""
    system_prompt = """Ты - эксперт по созданию презентаций. 
    Создавай структурированный и информативный контент для слайдов.
    Отвечай только на русском языке."""
    
    prompt = f"""Создай презентацию на тему "{topic}" из {num_slides} слайдов.
    
    Структура каждого слайда:
    1. Заголовок слайда
    2. Основной контент (2-4 пункта)
    
    Сделай презентацию информативной и интересной."""
    
    return await get_gpt_response(
        prompt, 
        system_prompt=system_prompt,
        temperature=0.8,
        max_tokens=2000
    )

async def improve_presentation_text(original_text: str) -> str:
    """Улучшает текст презентации"""
    system_prompt = """Ты - редактор презентаций. 
    Улучшай текст, делая его более читаемым и структурированным.
    Сохраняй оригинальный смысл."""
    
    prompt = f"""Улучши следующий текст презентации:
    
    {original_text}
    
    Сделай текст более структурированным, читаемым и профессиональным."""
    
    return await get_gpt_response(
        prompt,
        system_prompt=system_prompt,
        temperature=0.5
    )

async def analyze_presentation_content(content: str) -> Dict[str, Any]:
    """Анализирует контент презентации для подбора изображений"""
    system_prompt = """Ты - аналитик контента. 
    Анализируй текст и выдавай ключевые слова для поиска изображений.
    Отвечай в формате JSON."""
    
    prompt = f"""Проанализируй следующий контент презентации и выдели ключевые слова для поиска изображений:
    
    {content}
    
    Ответ в формате JSON:
    {{
        "keywords": ["ключевое слово 1", "ключевое слово 2"],
        "theme": "основная тема",
        "style": "предлагаемый стиль изображений"
    }}"""
    
    response = await get_gpt_response(
        prompt,
        system_prompt=system_prompt,
        temperature=0.3
    )
    
    try:
        import json
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "keywords": ["presentation", "business"],
            "theme": "general",
            "style": "professional"
        }
