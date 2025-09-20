"""
🖼️ Image Search Service
Асинхронный сервис для поиска изображений через Pexels API
Автор: SayDeck Team
"""

import asyncio
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import aiohttp
from config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

@dataclass
class ImageResult:
    """Результат поиска изображения"""
    id: int
    url: str
    original_url: str
    photographer: str
    photographer_url: str
    width: int
    height: int
    alt: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь для JSON"""
        return {
            "id": self.id,
            "url": self.url,
            "original_url": self.original_url,
            "photographer": self.photographer,
            "photographer_url": self.photographer_url,
            "width": self.width,
            "height": self.height,
            "alt": self.alt
        }

class PexelsImageService:
    """
    🎨 Современный асинхронный сервис для работы с Pexels API
    
    Возможности:
    - Поиск изображений по ключевым словам
    - Кэширование результатов
    - Обработка ошибок и fallback
    - Оптимизация размеров изображений
    - Автоматическая атрибуция авторов
    """
    
    BASE_URL = "https://api.pexels.com/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.PEXELS_API_KEY
        self.session: Optional[aiohttp.ClientSession] = None
        self._cache: Dict[str, List[ImageResult]] = {}
        
        if not self.api_key or self.api_key == "your_pexels_api_key":
            logger.warning("⚠️  Pexels API key не настроен. Изображения будут заменены плейсхолдерами")
    
    async def _ensure_session(self):
        """Создание HTTP сессии если она не существует"""
        if not self.session or self.session.closed:
            headers = {
                "Authorization": self.api_key,
                "User-Agent": "SayDeck/1.0.0"
            }
            timeout = aiohttp.ClientTimeout(total=10)
            self.session = aiohttp.ClientSession(
                headers=headers,
                timeout=timeout
            )
    
    async def search_images(
        self, 
        query: str, 
        per_page: int = 15,
        orientation: str = "landscape",
        size: str = "medium"
    ) -> List[ImageResult]:
        """
        🔍 Поиск изображений по запросу
        
        Args:
            query: Поисковый запрос
            per_page: Количество результатов (1-80)
            orientation: Ориентация (landscape, portrait, square)
            size: Размер (large, medium, small)
        
        Returns:
            Список найденных изображений
        """
        
        # Проверка кэша
        cache_key = f"{query}_{per_page}_{orientation}_{size}"
        if cache_key in self._cache:
            logger.info(f"📦 Возвращаем из кэша: {query}")
            return self._cache[cache_key]
        
        # Fallback если API key не настроен
        if not self.api_key or self.api_key == "your_pexels_api_key":
            logger.warning(f"🖼️  Генерируем плейсхолдер для: {query}")
            return await self._generate_placeholder_images(query, per_page)
        
        try:
            await self._ensure_session()
            
            params = {
                "query": query,
                "per_page": min(per_page, 80),  # Максимум 80
                "orientation": orientation,
                "size": size
            }
            
            logger.info(f"🔍 Поиск изображений: {query}")
            
            async with self.session.get(f"{self.BASE_URL}/search", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    images = await self._parse_images(data)
                    
                    # Кэшируем результат
                    self._cache[cache_key] = images
                    
                    logger.info(f"✅ Найдено {len(images)} изображений для: {query}")
                    return images
                
                elif response.status == 429:
                    logger.warning("⚠️  Превышен лимит запросов Pexels API")
                    return await self._generate_placeholder_images(query, per_page)
                
                else:
                    logger.error(f"❌ Ошибка Pexels API: {response.status}")
                    return await self._generate_placeholder_images(query, per_page)
                    
        except asyncio.TimeoutError:
            logger.error(f"⏰ Timeout при поиске изображений: {query}")
            return await self._generate_placeholder_images(query, per_page)
        
        except Exception as e:
            logger.error(f"💥 Ошибка при поиске изображений: {str(e)}")
            return await self._generate_placeholder_images(query, per_page)
    
    async def _parse_images(self, data: Dict) -> List[ImageResult]:
        """Парсинг ответа Pexels API в объекты ImageResult"""
        images = []
        
        for photo in data.get("photos", []):
            try:
                # Выбираем подходящий размер
                src = photo.get("src", {})
                url = src.get("large") or src.get("medium") or src.get("original")
                
                if url:
                    image = ImageResult(
                        id=photo.get("id"),
                        url=url,
                        original_url=photo.get("url"),
                        photographer=photo.get("photographer", "Unknown"),
                        photographer_url=photo.get("photographer_url", ""),
                        width=photo.get("width", 1920),
                        height=photo.get("height", 1080),
                        alt=photo.get("alt", "")
                    )
                    images.append(image)
                    
            except Exception as e:
                logger.error(f"💥 Ошибка парсинга изображения: {str(e)}")
                continue
        
        return images
    
    async def _generate_placeholder_images(self, query: str, count: int) -> List[ImageResult]:
        """
        🖼️  Генерация плейсхолдер изображений когда API недоступен
        """
        placeholders = []
        
        for i in range(min(count, 15)):
            # Разные размеры для разнообразия
            width = 1920 if i % 3 == 0 else 1280
            height = 1080 if i % 3 == 0 else 720
            
            placeholder = ImageResult(
                id=f"placeholder_{i}",
                url=f"https://via.placeholder.com/{width}x{height}/4A90E2/FFFFFF?text={query.replace(' ', '+')}", 
                original_url=f"https://via.placeholder.com/{width}x{height}",
                photographer="Placeholder Service",
                photographer_url="https://placeholder.com",
                width=width,
                height=height,
                alt=f"Placeholder image for {query}"
            )
            placeholders.append(placeholder)
        
        logger.info(f"🖼️  Сгенерировано {len(placeholders)} плейсхолдеров для: {query}")
        return placeholders
    
    async def get_image_by_id(self, image_id: int) -> Optional[ImageResult]:
        """
        📷 Получение конкретного изображения по ID
        """
        if not self.api_key or self.api_key == "your_pexels_api_key":
            return None
        
        try:
            await self._ensure_session()
            
            async with self.session.get(f"{self.BASE_URL}/photos/{image_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    images = await self._parse_images({"photos": [data]})
                    return images[0] if images else None
                
        except Exception as e:
            logger.error(f"💥 Ошибка получения изображения {image_id}: {str(e)}")
        
        return None
    
    def clear_cache(self):
        """🧹 Очистка кэша изображений"""
        self._cache.clear()
        logger.info("🧹 Кэш изображений очищен")
    
    async def search_for_slide_content(self, slide_content: str) -> Optional[ImageResult]:
        """
        🎯 Умный поиск изображения для содержимого слайда
        
        Анализирует текст слайда и находит наиболее подходящее изображение
        """
        
        # Извлекаем ключевые слова из содержимого
        keywords = await self._extract_keywords(slide_content)
        
        if not keywords:
            return None
        
        # Поиск изображений
        images = await self.search_images(keywords, per_page=5)
        
        # Возвращаем первое найденное изображение
        return images[0] if images else None
    
    async def _extract_keywords(self, text: str) -> str:
        """
        🧠 Простое извлечение ключевых слов из текста
        В будущем можно заменить на более продвинутый NLP
        """
        
        # Удаляем HTML теги если есть
        import re
        clean_text = re.sub(r'<[^>]+>', '', text)
        
        # Простая логика извлечения ключевых слов
        words = clean_text.lower().split()
        
        # Фильтруем стоп-слова (базовый набор)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'это', 'в', 'на', 'с', 'и', 'или', 'но', 'для', 'от', 'до', 'по'
        }
        
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        
        # Берем первые 2-3 ключевых слова
        return ' '.join(keywords[:3]) if keywords else text[:50]

    async def close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()

# Глобальный экземпляр сервиса
image_service = PexelsImageService()

async def search_images(query: str, count: int = 5) -> List[Dict[str, Any]]:
    """
    🚀 Быстрая функция для поиска изображений
    
    Usage:
        images = await search_images("nature sunset", 10)
    """
    async with image_service as service:
        results = await service.search_images(query, per_page=count)
        return [img.to_dict() for img in results]

async def get_image_for_slide(slide_content: str) -> Optional[Dict[str, Any]]:
    """
    🎯 Получение изображения для слайда
    
    Usage:
        image = await get_image_for_slide("Machine Learning algorithms")
    """
    async with image_service as service:
        result = await service.search_for_slide_content(slide_content)
        return result.to_dict() if result else None
