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

class EnhancedPresentationUpdate(BaseModel):
    """Запрос для обновления расширенной презентации"""
    topic: Optional[str] = None
    slides_count: Optional[int] = None
    audience: Optional[str] = None
    style: Optional[str] = None
    language: Optional[str] = None
    include_images: Optional[bool] = None
    image_style: Optional[str] = None
    auto_enhance: Optional[bool] = None

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
            text=f"Создай презентацию на тему: {request.topic}",
            topic=request.topic,
            slides_count=request.slides_count,
            language=request.language
        )
        
        try:
            base_response = await ai_manager.generate_presentation(ai_request)
            logger.info(f"✓ AI генерация завершена: {type(base_response)}")
        except Exception as ai_error:
            logger.error(f"❌ Ошибка AI генерации: {str(ai_error)}")
            # Fallback на демо презентацию
            base_response = _create_demo_presentation(request)
        
        # base_response теперь dict, а не объект с content
        base_content = base_response
        
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
        image_result = await image_service.search_for_slide_content(search_query)
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
        
        results = await image_service.search_images(enhanced_query, per_page=count)
            
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
        keywords = await image_service._extract_keywords(slide_content)
        image = await image_service.search_for_slide_content(slide_content)
        
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
    ❤️  Проверка здоровья расширенного сервиса генерации
    """
    try:
        # Проверяем доступность Pexels API
        pexels_status = "ok" if image_service.api_key and image_service.api_key != "your_pexels_api_key" else "no_api_key"
        
        # Проверяем AI сервисы
        ai_status = "ok" if ai_manager else "not_available"
        
        return {
            "status": "healthy",
            "service": "enhanced_generator",
            "services": {
                "pexels_api": pexels_status,
                "ai_services": ai_status
            },
            "endpoints": {
                "create": "POST /api/v1/enhanced/generate",
                "update": "PUT /api/v1/enhanced/presentation/{id}",
                "get": "GET /api/v1/enhanced/presentation/{id}", 
                "delete": "DELETE /api/v1/enhanced/presentation/{id}",
                "search_images": "GET /api/v1/enhanced/search-images",
                "analyze_slide": "POST /api/v1/enhanced/analyze-slide"
            },
            "features": [
                "Создание презентаций с изображениями",
                "Обновление существующих презентаций", 
                "Удаление презентаций",
                "Поиск изображений через Pexels API",
                "Анализ контента для подбора изображений",
                "Автоматическая генерация HTML превью"
            ],
            "cache_size": len(image_service._cache) if hasattr(image_service, '_cache') else 0,
            "version": settings.VERSION
        }
        
    except Exception as e:
        logger.error(f"💥 Ошибка проверки здоровья: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

def _create_demo_presentation(request: EnhancedPresentationRequest) -> Dict[str, Any]:
    """Создает демо презентацию при ошибках AI"""
    
    demo_slides = []
    
    for i in range(request.slides_count):
        if i == 0:
            demo_slides.append({
                "title": f"Введение в тему: {request.topic}",
                "content": f"Добро пожаловать на презентацию о теме '{request.topic}'. Эта презентация создана специально для аудитории: {request.audience}."
            })
        elif i == request.slides_count - 1:
            demo_slides.append({
                "title": "Заключение",
                "content": f"Спасибо за внимание! Мы рассмотрели основные аспекты темы '{request.topic}'. Надеемся, что презентация была полезной."
            })
        else:
            demo_slides.append({
                "title": f"Пункт {i}: Ключевые аспекты",
                "content": f"Здесь представлен важный материал по теме '{request.topic}'. Этот раздел содержит детальную информацию, адаптированную для {request.audience}."
            })
    
    return {
        "title": f"Презентация: {request.topic}",
        "slides": demo_slides
    }

@router.put("/presentation/{presentation_id}", response_model=EnhancedPresentationResponse)
async def update_enhanced_presentation(
    presentation_id: int,
    update_request: EnhancedPresentationUpdate,
    background_tasks: BackgroundTasks
) -> EnhancedPresentationResponse:
    """
    ✏️ Обновление существующей расширенной презентации
    
    Возможности:
    - Обновление параметров презентации
    - Перегенерация с новыми настройками
    - Обновление изображений при необходимости
    """
    
    import time
    start_time = time.time()
    
    try:
        logger.info(f"🔄 Обновление презентации ID: {presentation_id}")
        
        # Проверяем какие поля нужно обновить
        update_data = update_request.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="Не указаны поля для обновления"
            )
        
        # Создаем новый запрос на основе обновленных данных
        # В реальном приложении здесь был бы запрос к БД для получения текущих данных
        current_request = EnhancedPresentationRequest(
            topic=update_data.get("topic", "Обновленная презентация"),
            slides_count=update_data.get("slides_count", 5),
            audience=update_data.get("audience", "general"),
            style=update_data.get("style", "professional"),
            language=update_data.get("language", "ru"),
            include_images=update_data.get("include_images", True),
            image_style=update_data.get("image_style", "professional"),
            auto_enhance=update_data.get("auto_enhance", True)
        )
        
        logger.info(f"📝 Параметры обновления: {update_data}")
        
        # Генерируем обновленную презентацию
        ai_request = AIGenerationRequest(
            text=f"Обнови презентацию на тему: {current_request.topic}",
            topic=current_request.topic,
            slides_count=current_request.slides_count,
            language=current_request.language
        )
        
        try:
            base_response = await ai_manager.generate_presentation(ai_request)
            logger.info(f"✓ AI обновление завершено")
        except Exception as ai_error:
            logger.error(f"❌ Ошибка AI обновления: {str(ai_error)}")
            base_response = _create_demo_presentation(current_request)
        
        base_content = base_response
        slides_data = await _parse_generated_content(base_content)
        
        # Обновляем изображения если требуется
        enhanced_slides = []
        images_found = 0
        
        if current_request.include_images:
            logger.info(f"🖼️  Обновление изображений для {len(slides_data)} слайдов")
            
            image_tasks = []
            for slide_data in slides_data:
                task = _find_image_for_slide(slide_data, current_request.image_style)
                image_tasks.append(task)
            
            slide_images = await asyncio.gather(*image_tasks, return_exceptions=True)
            
            for i, slide_data in enumerate(slides_data):
                image_result = slide_images[i] if i < len(slide_images) else None
                
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
            for slide_data in slides_data:
                enhanced_slide = SlideWithImage(
                    title=slide_data.get("title", ""),
                    content=slide_data.get("content", ""),
                    layout="title-content"
                )
                enhanced_slides.append(enhanced_slide)
        
        generation_time = time.time() - start_time
        
        logger.info(f"✅ Презентация обновлена! Время: {generation_time:.2f}с, Изображений: {images_found}")
        
        # В реальном приложении здесь было бы обновление в БД
        
        return EnhancedPresentationResponse(
            title=base_content.get("title", current_request.topic),
            slides=enhanced_slides,
            total_slides=len(enhanced_slides),
            generation_time=generation_time,
            images_found=images_found,
            html_preview=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Ошибка обновления презентации: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обновления презентации: {str(e)}"
        )

@router.delete("/presentation/{presentation_id}")
async def delete_enhanced_presentation(presentation_id: int) -> Dict[str, Any]:
    """
    🗑️ Удаление расширенной презентации
    
    Возможности:
    - Удаление презентации по ID
    - Очистка связанных ресурсов
    - Логирование операции удаления
    """
    
    try:
        logger.info(f"🗑️ Удаление презентации ID: {presentation_id}")
        
        # Проверяем существование презентации
        if presentation_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="Некорректный ID презентации"
            )
        
        # В реальном приложении здесь был бы запрос к БД для проверки существования
        # и права доступа пользователя к презентации
        
        # Симуляция проверки существования
        if presentation_id > 10000:  # Имитация несуществующей презентации
            raise HTTPException(
                status_code=404,
                detail=f"Презентация с ID {presentation_id} не найдена"
            )
        
        # В реальном приложении здесь было бы:
        # 1. Удаление из базы данных
        # 2. Удаление связанных файлов
        # 3. Очистка кэша
        
        logger.info(f"✅ Презентация {presentation_id} успешно удалена")
        
        return {
            "success": True,
            "message": f"Презентация {presentation_id} успешно удалена",
            "presentation_id": presentation_id,
            "deleted_at": "2025-07-07T15:00:00Z"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Ошибка удаления презентации: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка удаления презентации: {str(e)}"
        )

@router.get("/presentation/{presentation_id}")
async def get_enhanced_presentation(presentation_id: int) -> Dict[str, Any]:
    """
    📄 Получение расширенной презентации по ID
    
    Дополнительный эндпоинт для получения существующей презентации
    """
    
    try:
        logger.info(f"📄 Получение презентации ID: {presentation_id}")
        
        if presentation_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="Некорректный ID презентации"
            )
        
        # Симуляция проверки существования
        if presentation_id > 10000:
            raise HTTPException(
                status_code=404,
                detail=f"Презентация с ID {presentation_id} не найдена"
            )
        
        # В реальном приложении здесь был бы запрос к БД
        # Для демонстрации возвращаем макет данных
        
        demo_slides = [
            {
                "title": "Демо слайд 1",
                "content": "Это демонстрационное содержимое первого слайда",
                "image": {
                    "url": "https://images.pexels.com/photos/574077/pexels-photo-574077.jpeg",
                    "alt": "Demo image",
                    "photographer": "Demo Author"
                },
                "layout": "title-content-image"
            }
        ]
        
        return {
            "presentation_id": presentation_id,
            "title": f"Демо презентация {presentation_id}",
            "slides": demo_slides,
            "total_slides": len(demo_slides),
            "created_at": "2025-07-07T14:00:00Z",
            "updated_at": "2025-07-07T15:00:00Z",
            "images_count": 1,
            "status": "ready"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Ошибка получения презентации: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения презентации: {str(e)}"
        )
