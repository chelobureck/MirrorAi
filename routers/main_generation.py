"""
Main Generation Router - основной эндпоинт для генерации презентаций по ТЗ
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, Header, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import asyncio

from models.base import get_session
from models.user import User
from utils.auth import get_current_user_optional
from schemas.generation import (
    PresentationGenerateRequest,
    PresentationGenerateResponse,
    ErrorResponse,
    GuestCreditsInfo
)
from services.guest_credits import guest_credits_service
from services.presentation_files import presentation_files_service
from services.image_microservice import image_microservice_client
from ai_services.manager import ai_manager
from services.template_service import TemplateService
from ai_services.image_service import image_service, get_image_for_slide

router = APIRouter(tags=["Main Generation"])

@router.post(
    "/generate-presentation",
    response_model=PresentationGenerateResponse,
    responses={
        403: {"model": ErrorResponse, "description": "Not enough credits"},
        500: {"model": ErrorResponse, "description": "Generation error"}
    }
)
async def generate_presentation(
    request: PresentationGenerateRequest,
    req: Request,
    session: AsyncSession = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_user_optional),
    x_guest_session: Optional[str] = Header(None, alias="X-Guest-Session"),
    template_id: Optional[str] = Body(None, description="ID шаблона для генерации")
):
    """
    🎯 Основной эндпоинт для генерации презентаций
    
    **Логика:**
    1. Проверить регистрацию (авторизованный пользователь или гость)
    2. Для гостя - проверить и списать кредит
    3. Сгенерировать HTML-презентацию (без фото)
    4. Сохранить черновой HTML
    5. Отправить в микросервис картинок
    6. Получить финальный HTML с рабочими URL картинок
    7. Сохранить финальный вариант
    8. Вернуть результат
    """
    
    # Определяем пользователя или гостя
    user_id = None
    guest_session_id = None
    
    if current_user:
        # Авторизованный пользователь - генерация без ограничений
        user_id = str(current_user.id)
        user_or_guest_id = f"user_{user_id}"
    else:
        # Гость - работаем с кредитами
        ip_address = req.client.host
        user_agent = req.headers.get("User-Agent", "")
        
        # Получаем или создаем гостевую сессию
        guest_session_id, credits = await guest_credits_service.get_or_create_guest_session(
            x_guest_session, ip_address, user_agent, session
        )
        
        # Проверяем кредиты
        if credits <= 0:
            return JSONResponse(
                status_code=403,
                content={"error": "Not enough credits"}
            )
        
        # Списываем кредит
        credit_used = await guest_credits_service.use_credit(guest_session_id, session)
        if not credit_used:
            return JSONResponse(
                status_code=403,
                content={"error": "Not enough credits"}
            )
        
        user_or_guest_id = f"guest_{guest_session_id}"
    
    try:
        # Генерируем уникальный ID презентации
        presentation_id = str(uuid.uuid4())
        
        # 1. Генерируем HTML-презентацию (без фото)
        # Используем глобальный ai_manager
        
        # Формируем запрос к AI
        generation_request = {
            "topic": request.topic,
            "content": request.content or "",
            "slides_count": request.slides_count,
            "language": request.language,
            "with_images": False  # Пока без картинок
        }
        
        # Генерируем презентацию
        raw_presentation = await ai_manager.generate_presentation(generation_request)
        
        # Извлекаем слайды и заголовок
        slides = raw_presentation.get("slides") if isinstance(raw_presentation, dict) else None
        title = raw_presentation.get("title") if isinstance(raw_presentation, dict) else request.topic
        
        # --- Новый блок: подбор изображений для слайдов ---
        if slides:
            image_tasks = []
            for slide in slides:
                search_query = f"{slide.get('title','')} {slide.get('content','')}"
                image_tasks.append(get_image_for_slide(search_query))
            images = await asyncio.gather(*image_tasks)
            for i, slide in enumerate(slides):
                image = images[i] if i < len(images) else None
                if image:
                    slide['image'] = image.to_dict() if hasattr(image, 'to_dict') else image
        # --- Конец блока ---
        
        # Если выбран шаблон, подставляем контент в шаблон
        if template_id:
            # Сначала ищем встроенный шаблон
            builtin = TemplateService.get_builtin_template(template_id)
            template_html = None
            if builtin:
                template_html = builtin['html_content']
            else:
                template_html = await TemplateService.get_template_html(template_id, session)
            if template_html:
                slides_html = ""
                if slides:
                    for i, slide in enumerate(slides):
                        # Вставка изображения, если есть
                        img_html = ""
                        if slide.get('image') and slide['image'].get('url'):
                            img_html = f"<div class='slide-image'><img src='{slide['image']['url']}' alt='{slide['image'].get('alt','')}' /><div class='image-credit'>Фото: {slide['image'].get('photographer','')} | Pexels</div></div>"
                        slides_html += f"<div class='slide'><h2>{slide.get('title','')}</h2><div class='content'>{slide.get('content','')}</div>{img_html}</div>"
                else:
                    slides_html = "<div class='slide'><h2>Нет слайдов</h2></div>"
                raw_html = template_html.replace("{{slides}}", slides_html).replace("{{title}}", title)
            else:
                raw_html = await _create_fallback_html(request)
        else:
            if isinstance(raw_presentation, dict) and "html" in raw_presentation:
                raw_html = raw_presentation["html"]
            else:
                raw_html = await _create_fallback_html(request)
        
        # 2. Сохраняем черновой HTML
        await presentation_files_service.save_raw_html(
            user_or_guest_id, presentation_id, raw_html
        )
        
        # 3. Отправляем в микросервис картинок
        final_html = await image_microservice_client.process_html_with_images(
            raw_html, request.topic
        )
        
        # 4. Сохраняем финальный HTML
        await presentation_files_service.save_final_html(
            user_or_guest_id, presentation_id, final_html
        )
        
        # 5. Формируем ответ
        response = PresentationGenerateResponse(
            presentation_id=presentation_id,
            html=final_html
        )
        
        # Добавляем заголовок с session_id для гостей
        response_json = response.model_dump()
        headers = {}
        
        if guest_session_id:
            headers["X-Guest-Session"] = guest_session_id
            remaining_credits = await guest_credits_service.get_credits(guest_session_id, session)
            headers["X-Guest-Credits"] = str(remaining_credits)
        
        if not current_user and x_guest_session:
            response_json["guest_session_id"] = x_guest_session
        
        return JSONResponse(content=response_json, headers=headers)
        
    except Exception as e:
        # В случае ошибки - возвращаем кредит гостю
        if guest_session_id:
            await guest_credits_service.refund_credit(guest_session_id, session)
        
        return JSONResponse(
            status_code=500,
            content={"error": f"Generation failed: {str(e)}"}
        )

@router.get("/guest-credits", response_model=GuestCreditsInfo)
async def get_guest_credits(
    req: Request,
    session: AsyncSession = Depends(get_session),
    x_guest_session: Optional[str] = Header(None, alias="X-Guest-Session")
):
    """Получить информацию о кредитах гостя"""
    
    if not x_guest_session:
        return JSONResponse(
            status_code=400,
            content={"error": "X-Guest-Session header required"}
        )
    
    credits = await guest_credits_service.get_credits(x_guest_session, session)
    
    return GuestCreditsInfo(
        session_id=x_guest_session,
        credits=credits,
        credits_used=50 - credits
    )

async def _create_fallback_html(request: PresentationGenerateRequest) -> str:
    """Создать простой HTML в случае отказа AI сервиса"""
    slides_html = ""
    
    for i in range(request.slides_count):
        slide_title = f"Слайд {i + 1}"
        if i == 0:
            slide_title = request.topic
        
        slides_html += f"""
        <div class="slide">
            <h2>{slide_title}</h2>
            <div class="content">
                <p>Содержимое слайда {i + 1}</p>
                {f'<p>{request.content}</p>' if request.content and i == 1 else ''}
            </div>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html lang="{request.language}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{request.topic}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
            .slide {{ background: white; margin: 20px 0; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h2 {{ color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
            .content {{ margin-top: 20px; line-height: 1.6; }}
        </style>
    </head>
    <body>
        <h1>{request.topic}</h1>
        {slides_html}
    </body>
    </html>
    """
