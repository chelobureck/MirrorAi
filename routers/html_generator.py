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
html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    body {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #333;
    }}
    
    .presentation-container {{
        width: 90%;
        max-width: 900px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        position: relative;
    }}
    
    .presentation-header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        text-align: center;
    }}
    
    .presentation-title {{
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }}
    
    .slide {{
        display: none;
        padding: 40px;
        min-height: 500px;
        animation: fadeIn 0.5s ease-in-out;
    }}
    
    .slide.active {{
        display: block;
    }}
    
    .slide-content h1 {{
        color: #667eea;
        font-size: 2.2rem;
        margin-bottom: 20px;
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
    }}
    
    .slide-content h2 {{
        color: #764ba2;
        font-size: 1.8rem;
        margin-bottom: 15px;
        margin-top: 25px;
    }}
    
    .slide-content h3 {{
        color: #667eea;
        font-size: 1.4rem;
        margin-bottom: 12px;
        margin-top: 20px;
    }}
    
    .slide-content p {{
        font-size: 1.1rem;
        line-height: 1.7;
        margin-bottom: 15px;
        color: #555;
    }}
    
    .slide-content strong {{
        color: #667eea;
        font-weight: 600;
    }}
    
    .slide-content em {{
        color: #764ba2;
        font-style: italic;
    }}
    
    .slide-content ul {{
        margin: 20px 0;
        padding-left: 0;
    }}
    
    .slide-content li {{
        list-style: none;
        margin: 12px 0;
        padding: 12px 20px;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8edff 100%);
        border-left: 4px solid #667eea;
        border-radius: 8px;
        font-size: 1.05rem;
        position: relative;
    }}
    
    .slide-content li:before {{
        content: "→";
        color: #667eea;
        font-weight: bold;
        margin-right: 10px;
    }}
    
    .slide-title {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 60px 40px;
    }}
    
    .slide-conclusion {{
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        color: white;
        padding: 40px;
    }}
    
    .slide-conclusion h1,
    .slide-conclusion h2,
    .slide-conclusion h3 {{
        color: white;
    }}
    
    .navigation {{
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 10px;
    }}
    
    .nav-btn {{
        background: #667eea;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }}
    
    .nav-btn:hover {{
        background: #5a67d8;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }}
    
    .nav-btn:disabled {{
        background: #ccc;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }}
    
    .slide-counter {{
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba(102, 126, 234, 0.1);
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 14px;
        color: #667eea;
        font-weight: 500;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @media (max-width: 768px) {{
        .presentation-container {{ width: 95%; }}
        .slide {{ padding: 20px; }}
        .presentation-title {{ font-size: 2rem; }}
        .slide-content h1 {{ font-size: 1.8rem; }}
    }}
</style>
</head>
<body>
<div class="presentation-container">
    <div class="presentation-header">
        <h1 class="presentation-title">{title}</h1>
        <div class="slide-counter">
            <span id="current-slide">1</span> / <span id="total-slides">{len(slides)}</span>
        </div>
    </div>
    
    <div class="slides-container">
        {slides_html}
    </div>
</div>

</body>
</html>
"""

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
