"""
HTML Generator Router - создание презентаций с полным HTML выводом
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import HTMLResponse
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from models.base import get_session
from models import User
from models.presentation import Presentation
from utils.auth import get_current_user
from ai_services import ai_manager, AIGenerationRequest

router = APIRouter(prefix="/generate", tags=["html-generation"])

def create_modern_html_presentation(presentation_data: Dict[str, Any]) -> str:
    """Создает полную HTML страницу с современными стилями"""

    title = presentation_data.get("title", "Презентация")
    slides = presentation_data.get("slides", [])

    # Генерируем HTML для слайдов
    slides_html = ""
    for i, slide in enumerate(slides):
        slide_title = slide.get("title", "")
        slide_content = slide.get("content", "")
        slide_type = slide.get("type", "content")
        
        # Добавляем класс для типа слайда
        slide_class = f"slide slide-{slide_type}"
        if i == 0:
            slide_class += " active"
            
        slides_html += f"""
        <div class="{slide_class}" data-slide="{i}">
            <div class="slide-content">
                {slide_title}
                {slide_content}
            </div>
        </div>
        """

    # Создаем полную HTML страницу с современными стилями
    html_content = f""""""  

    return html_content


@router.post("/", response_class=HTMLResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def generate_html_presentation(
    text: str = Body(..., description="Текст для создания презентации"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Генерирует презентацию в виде полной HTML страницы через Groq"""
    
    if not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Текст не может быть пустым"
        )
    
    try:
        # Создаем запрос для AI (Groq сам определит параметры)
        ai_request = AIGenerationRequest(
            text=f"You are an AI slide deck generator that outputs a complete HTML document for a web presentation. Your task:🎯 Generate a modern, professional, multi-slide HTML presentation on the topic {text} (replace with the actual topic).Strict Instructions:✅ Output only valid, well-formed, production-ready HTML. No explanations, no extra text outside the HTML document.✅ Each slide must be in its own <section> tag with a clear and consistent style.✅ Each slide must contain:A clear, professional <h1> title.An optional <h2> subtitle if helpful.A <p> with at least 40 words of informative, professional content.An <img> tag with a data-search-keywords attribute instead of a real src. The keywords must be in English, specific and descriptive, so they can be used to search relevant images on Pexels API. Do not use any static URLs or placeholder images.✅ The design must use a clean, light, professional color palette suitable for business or educational presentations (e.g. whites, light grays, light blues).✅ Include at least slides (e.g. 5–7), covering different aspects of the topic in depth.✅ Make sure the keywords in data-search-keywords are specific enough to return highly relevant images from Pexels.✅ Your final answer must be only the complete, production-ready HTML document. Do not include any explanations or instructions outside the HTML.Example slide (only for guidance):<section style="background-color:#F8FAFC;"><img data-search-keywords="modern business meeting technology"><h1>Modern Business Meetings</h1><h2>Technology and Collaboration</h2><p>Business meetings have evolved dramatically thanks to new communication technologies. Tools such as video conferencing and collaborative platforms have made remote work effective, enabling companies to reduce costs and increase flexibility.</p></section>You must generate a full HTML document with multiple slides following these instructions exactly.",
            language="ru",
            slides_count=5,  # Заглушка, Groq сам определит
            animation=False
        )
        
        # Генерируем презентацию через Groq
        presentation_data = await ai_manager.generate_presentation(ai_request)
        
        # Создаем HTML страницу
        #html_content = create_modern_html_presentation(presentation_data)
        
        # Сохраняем в базу данных
        new_presentation = Presentation(
            title=presentation_data.get("title", "Сгенерированная презентация"),
            content=presentation_data,  # JSON структура
            user_id=current_user.id
        )
        session.add(new_presentation)
        await session.commit()
        await session.refresh(new_presentation)
        
        print(f"✅ Презентация создана: ID={new_presentation.id}, User={current_user.id}")
        
        # Возвращаем HTML
        return HTMLResponse(
            content=html_content,
            status_code=200,
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "X-Presentation-ID": str(new_presentation.id)
            }
        )
        
    except Exception as e:
        print(f"❌ Ошибка генерации презентации: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка генерации презентации: {str(e)}"
        )

@router.post("/json", dependencies=[Depends(RateLimiter(times=15, seconds=60))])
async def generate_json_presentation(
    text: str = Body(..., description="Текст для создания презентации"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Генерирует презентацию в JSON формате (для API интеграций)"""
    
    if not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Текст не может быть пустым"
        )
    
    try:
        # Создаем запрос для AI
        ai_request = AIGenerationRequest(
            text="""You are an AI slide deck generator that outputs a complete HTML document for a web presentation.

Your task:

🎯 Generate a modern, professional, multi-slide HTML presentation on the topic "{{text}}" (replace with the actual topic).

Strict Instructions:

✅ Output only valid, well-formed, production-ready HTML. No explanations, no extra text outside the HTML document.

✅ Each slide must be in its own <section> tag with a clear and consistent style.

✅ Each slide must contain:
A clear, professional <h1> title.
An optional <h2> subtitle if helpful.
A <p> with at least 40 words of informative, professional content.
An <img> tag with a data-search-keywords attribute instead of a real src. The keywords must be in English, specific and descriptive, so they can be used to search relevant images on Pexels API. Do not use any static URLs or placeholder images.

✅ The design must use a clean, light, professional color palette suitable for business or educational presentations (e.g. whites, light grays, light blues).

✅ Include at least slides (e.g. 5–7), covering different aspects of the topic in depth.

✅ Make sure the keywords in data-search-keywords are specific enough to return highly relevant images from Pexels.

✅ Your final answer must be only the complete, production-ready HTML document. Do not include any explanations or instructions outside the HTML.

Example slide (only for guidance):

<section style="background-color:#F8FAFC;">
  <img data-search-keywords="modern business meeting technology">
  <h1>Modern Business Meetings</h1>
  <h2>Technology and Collaboration</h2>
  <p>Business meetings have evolved dramatically thanks to new communication technologies. Tools such as video conferencing and collaborative platforms have made remote work effective, enabling companies to reduce costs and increase flexibility.</p>
</section>

You must generate a full HTML document with multiple slides following these instructions exactly.""",
            language="ru",
            slides_count=5,  # Groq сам определит
            animation=False
        )
        
        # Генерируем презентацию через Groq
        presentation_data = await ai_manager.generate_presentation(ai_request)
        
        # Сохраняем в базу данных
        new_presentation = Presentation(
            title=presentation_data.get("title", "Сгенерированная презентация"),
            content=presentation_data,
            user_id=current_user.id
        )
        session.add(new_presentation)
        await session.commit()
        await session.refresh(new_presentation)
        
        # Возвращаем JSON с ID презентации
        return {
            "presentation_id": new_presentation.id,
            "title": presentation_data.get("title"),
            "slides_count": len(presentation_data.get("slides", [])),
            "content": presentation_data,
            "created_at": new_presentation.created_at.isoformat(),
            "message": "Презентация успешно создана"
        }
        
    except Exception as e:
        print(f"❌ Ошибка генерации презентации: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка генерации презентации: {str(e)}"
        )
