"""
🚀 Enhanced Presentation Generator
Роутер для генерации презентаций с автоматическим поиском и вставкой изображений
Автор: SayDeck Team
"""

import logging
import asyncio
import json
import re
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ai_services.image_service import image_service, get_image_for_slide
from ai_services.manager import ai_manager
from ai_services import AIGenerationRequest, AIProviderType
from config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/enhanced", tags=["Enhanced Generation"])

class EnhancedPresentationRequest(BaseModel):
    """Запрос для создания расширенной презентации"""
    topic: str
    slides_count: int = 5
    audience: str = "general"
    style: str = "professional"
    language: str = "ru"
    include_images: bool = True
    image_style: str = "professional"  # professional, creative, minimal
    auto_enhance: bool = True

class SlideWithImage(BaseModel):
    """Слайд с изображением"""
    title: str
    content: str
    image: Optional[Dict[str, Any]] = None
    image_alt: str = ""
    layout: str = "title-content-image"

class EnhancedPresentationResponse(BaseModel):
    """Ответ с расширенной презентацией"""
    title: str
    slides: List[SlideWithImage]
    total_slides: int
    generation_time: float
    images_found: int
    html_preview: Optional[str] = None

@router.post("/generate", response_model=EnhancedPresentationResponse)
async def generate_enhanced_presentation(
    request: EnhancedPresentationRequest,
    background_tasks: BackgroundTasks
) -> EnhancedPresentationResponse:
    """
    🎨 Генерация презентации с автоматическим поиском изображений
    
    Возможности:
    - Автоматический поиск релевантных изображений для каждого слайда
    - Умная обработка контента для оптимального поиска
    - Fallback на плейсхолдеры при недоступности API
    - Генерация HTML превью
    """
    
    import time
    start_time = time.time()
    
    try:
        logger.info(f"🚀 Генерация расширенной презентации: {request.topic}")
        
        # 1. Генерируем базовую презентацию через AI manager
        ai_request = AIGenerationRequest(
            text=f"""Создай структурированную презентацию на тему: {request.topic}
            
Аудитория: {request.audience}
Стиль: {request.style}
Количество слайдов: {request.slides_count}
Язык: {request.language}

Верни ответ в JSON формате:
{{
    \"title\": \"Название презентации\",
    \"slides\": [
        {{
            \"title\": \"Заголовок слайда\",
            \"content\": \"Содержимое слайда\"
        }}
    ]
}}""",
            language=request.language
        )
        
        base_response = await ai_manager.generate_content(ai_request)
        
        # Парсим JSON ответ
        try:
            import json
            base_content = json.loads(base_response.content)
        except json.JSONDecodeError:
            # Fallback - создаем простую структуру
            base_content = {
                "title": request.topic,
                "slides": [
                    {
                        "title": f"Слайд о {request.topic}",
                        "content": base_response.content[:500]
                    }
                ]
            }
        
        # 2. Парсим сгенерированный контент
        slides_data = await _parse_generated_content(base_content)
        
        # 3. Добавляем изображения к каждому слайду
        enhanced_slides = []
        images_found = 0
        
        if request.include_images:
            logger.info(f"🖼️  Поиск изображений для {len(slides_data)} слайдов")
            
            # Параллельный поиск изображений для всех слайдов
            image_tasks = []
            for slide_data in slides_data:
                task = _find_image_for_slide(slide_data, request.image_style)
                image_tasks.append(task)
            
            # Ждем завершения всех задач поиска
            slide_images = await asyncio.gather(*image_tasks, return_exceptions=True)
            
            # Собираем результаты
            for i, slide_data in enumerate(slides_data):
                image_result = slide_images[i] if i < len(slide_images) else None
                
                # Проверяем что это не исключение
                if isinstance(image_result, Exception):
                    logger.error(f"❌ Ошибка поиска изображения для слайда {i}: {str(image_result)}")
                    image_result = None
                
                if image_result:
                    images_found += 1
                
                enhanced_slide = SlideWithImage(
                    title=slide_data.get("title", ""),
                    content=slide_data.get("content", ""),
                    image=image_result,
                    image_alt=image_result.get("alt", "") if image_result else "",
                    layout="title-content-image" if image_result else "title-content"
                )
                enhanced_slides.append(enhanced_slide)
        else:
            # Создаем слайды без изображений
            for slide_data in slides_data:
                enhanced_slide = SlideWithImage(
                    title=slide_data.get("title", ""),
                    content=slide_data.get("content", ""),
                    layout="title-content"
                )
                enhanced_slides.append(enhanced_slide)
        
        # 4. Генерируем HTML превью в фоне
        html_preview = None
        if request.auto_enhance:
            background_tasks.add_task(
                _generate_html_preview, 
                enhanced_slides, 
                base_content.get("title", request.topic)
            )
        
        generation_time = time.time() - start_time
        
        logger.info(f"✅ Презентация готова! Время: {generation_time:.2f}с, Изображений: {images_found}")
        
        return EnhancedPresentationResponse(
            title=base_content.get("title", request.topic),
            slides=enhanced_slides,
            total_slides=len(enhanced_slides),
            generation_time=generation_time,
            images_found=images_found,
            html_preview=html_preview
        )
        
    except Exception as e:
        logger.error(f"💥 Ошибка генерации презентации: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Ошибка генерации презентации: {str(e)}"
        )

async def _parse_generated_content(content: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    📝 Парсинг сгенерированного контента в структурированные слайды
    """
    slides = []
    
    try:
        # Если контент уже структурирован
        if "slides" in content:
            return content["slides"]
        
        # Если это просто текст, разбиваем на слайды
        text_content = content.get("content", str(content))
        
        # Простой парсинг по заголовкам
        slide_sections = re.split(r'\n(?=#{1,3}\s)', text_content)
        
        for section in slide_sections:
            if not section.strip():
                continue
                
            lines = section.strip().split('\n')
            title = lines[0].strip('#').strip() if lines else ""
            content_lines = lines[1:] if len(lines) > 1 else []
            content = '\n'.join(content_lines).strip()
            
            if title:
                slides.append({
                    "title": title,
                    "content": content
                })
        
        # Если парсинг не сработал, создаем один слайд
        if not slides:
            slides.append({
                "title": content.get("title", "Презентация"),
                "content": text_content
            })
            
    except Exception as e:
        logger.error(f"💥 Ошибка парсинга контента: {str(e)}")
        # Fallback
        slides.append({
            "title": "Презентация", 
            "content": str(content)
        })
    
    return slides

async def _find_image_for_slide(slide_data: Dict[str, str], style: str) -> Optional[Dict[str, Any]]:
    """
    🔍 Поиск изображения для конкретного слайда
    """
    try:
        title = slide_data.get("title", "")
        content = slide_data.get("content", "")
        
        # Создаем поисковый запрос из заголовка и контента
        search_query = f"{title} {content}"
        
        # Добавляем стилевые модификаторы
        if style == "professional":
            search_query += " business professional"
        elif style == "creative":
            search_query += " creative modern design"
        elif style == "minimal":
            search_query += " minimal clean simple"
        
        # Ищем изображение
        async with image_service as service:
            image_result = await service.search_for_slide_content(search_query)
            return image_result.to_dict() if image_result else None
            
    except Exception as e:
        logger.error(f"💥 Ошибка поиска изображения: {str(e)}")
        return None

async def _generate_html_preview(slides: List[SlideWithImage], title: str):
    """
    🎨 Генерация HTML превью презентации (выполняется в фоне)
    """
    try:
        logger.info(f"🎨 Генерация HTML превью для: {title}")
        
        html_template = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .presentation {{ max-width: 1200px; margin: 0 auto; }}
                .slide {{ background: white; margin: 20px 0; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .slide-title {{ font-size: 24px; font-weight: bold; color: #333; margin-bottom: 15px; border-bottom: 2px solid #4A90E2; padding-bottom: 10px; }}
                .slide-content {{ font-size: 16px; line-height: 1.6; color: #666; margin-bottom: 20px; }}
                .slide-image {{ text-align: center; margin: 20px 0; }}
                .slide-image img {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .image-credit {{ font-size: 12px; color: #999; margin-top: 5px; }}
                .header {{ text-align: center; margin-bottom: 40px; }}
                .header h1 {{ color: #333; font-size: 36px; margin-bottom: 10px; }}
                .header p {{ color: #666; font-size: 18px; }}
            </style>
        </head>
        <body>
            <div class="presentation">
                <div class="header">
                    <h1>{title}</h1>
                    <p>Сгенерировано с помощью SayDeck AI</p>
                </div>
                {slides_html}
            </div>
        </body>
        </html>
        """
        
        slides_html = ""
        for i, slide in enumerate(slides, 1):
            slide_html = f"""
            <div class="slide">
                <div class="slide-title">{i}. {slide.title}</div>
                <div class="slide-content">{slide.content.replace(chr(10), '<br>')}</div>
            """
            
            if slide.image:
                slide_html += f"""
                <div class="slide-image">
                    <img src="{slide.image['url']}" alt="{slide.image_alt}" />
                    <div class="image-credit">
                        Фото: {slide.image['photographer']} | Источник: Pexels
                    </div>
                </div>
                """
            
            slide_html += "</div>"
            slides_html += slide_html
        
        final_html = html_template.format(
            title=title,
            slides_html=slides_html
        )
        
        # Сохраняем в файл или кэш (опционально)
        logger.info(f"✅ HTML превью готов")
        
        return final_html
        
    except Exception as e:
        logger.error(f"💥 Ошибка генерации HTML превью: {str(e)}")
        return None

@router.get("/search-images")
async def search_images_endpoint(
    query: str, 
    count: int = 10,
    style: str = "professional"
) -> Dict[str, Any]:
    """
    🔍 API для поиска изображений
    """
    try:
        # Добавляем стилевые модификаторы
        enhanced_query = query
        if style == "professional":
            enhanced_query += " business professional"
        elif style == "creative":
            enhanced_query += " creative modern design"
        elif style == "minimal":
            enhanced_query += " minimal clean"
        
        async with image_service as service:
            results = await service.search_images(enhanced_query, per_page=count)
            
        return {
            "query": query,
            "enhanced_query": enhanced_query,
            "count": len(results),
            "images": [img.to_dict() for img in results]
        }
        
    except Exception as e:
        logger.error(f"💥 Ошибка поиска изображений: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-slide")
async def analyze_slide_for_image(slide_content: str) -> Dict[str, Any]:
    """
    🧠 Анализ слайда для подбора изображения
    """
    try:
        async with image_service as service:
            # Извлекаем ключевые слова
            keywords = await service._extract_keywords(slide_content)
            
            # Ищем изображение
            image = await service.search_for_slide_content(slide_content)
            
        return {
            "original_content": slide_content,
            "extracted_keywords": keywords,
            "suggested_image": image.to_dict() if image else None
        }
        
    except Exception as e:
        logger.error(f"💥 Ошибка анализа слайда: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    ❤️  Проверка здоровья сервиса
    """
    try:
        # Проверяем доступность Pexels API
        pexels_status = "ok" if image_service.api_key and image_service.api_key != "your_pexels_api_key" else "no_api_key"
        
        # Проверяем AI сервисы
        ai_status = "ok" if ai_manager else "not_available"
        
        return {
            "status": "healthy",
            "services": {
                "pexels_api": pexels_status,
                "ai_services": ai_status
            },
            "cache_size": len(image_service._cache),
            "version": settings.VERSION
        }
        
    except Exception as e:
        logger.error(f"💥 Ошибка проверки здоровья: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }
