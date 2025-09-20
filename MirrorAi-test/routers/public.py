"""
Роутер для публичных презентаций с шарингом
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.base import get_session
from models.user import User
from models.presentation import Presentation
from schemas.presentation import PresentationResponse
from utils.auth import get_current_user
from typing import Optional
import uuid
from datetime import datetime

router = APIRouter(prefix="/public", tags=["public"])

@router.post("/presentations/{presentation_id}/share")
async def make_presentation_public(
    presentation_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Сделать презентацию публичной и получить ссылку для шаринга"""
    
    # Проверяем, что презентация принадлежит пользователю
    result = await session.execute(
        select(Presentation).where(
            Presentation.id == presentation_id,
            Presentation.user_id == current_user.id
        )
    )
    presentation = result.scalars().first()
    
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Презентация не найдена"
        )
    
    # Генерируем уникальный публичный ID
    public_id = str(uuid.uuid4())
    
    # Обновляем презентацию
    await session.execute(
        update(Presentation)
        .where(Presentation.id == presentation_id)
        .values(
            is_public=True,
            public_id=public_id,
            shared_at=datetime.utcnow()
        )
    )
    await session.commit()
    
    return {
        "message": "Презентация стала публичной",
        "public_id": public_id,
        "public_url": f"/public/presentations/{public_id}",
        "share_url": f"http://localhost:8000/public/presentations/{public_id}"
    }

@router.delete("/presentations/{presentation_id}/share")
async def make_presentation_private(
    presentation_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Сделать презентацию приватной"""
    
    result = await session.execute(
        select(Presentation).where(
            Presentation.id == presentation_id,
            Presentation.user_id == current_user.id
        )
    )
    presentation = result.scalars().first()
    
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Презентация не найдена"
        )
    
    await session.execute(
        update(Presentation)
        .where(Presentation.id == presentation_id)
        .values(
            is_public=False,
            public_id=None
        )
    )
    await session.commit()
    
    return {"message": "Презентация стала приватной"}

@router.get("/presentations/{public_id}", response_model=PresentationResponse)
async def get_public_presentation(
    public_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Получить публичную презентацию по публичному ID"""
    
    result = await session.execute(
        select(Presentation).where(
            Presentation.public_id == public_id,
            Presentation.is_public == True
        )
    )
    presentation = result.scalars().first()
    
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Публичная презентация не найдена"
        )
    
    # Увеличиваем счетчик просмотров
    await session.execute(
        update(Presentation)
        .where(Presentation.id == presentation.id)
        .values(views_count=(Presentation.views_count or 0) + 1)
    )
    await session.commit()
    
    return presentation

@router.get("/presentations/{public_id}/viewer", response_class=HTMLResponse)
async def view_public_presentation(
    public_id: str,
    session: AsyncSession = Depends(get_session)
):
    """HTML страница для просмотра публичной презентации"""
    
    result = await session.execute(
        select(Presentation).where(
            Presentation.public_id == public_id,
            Presentation.is_public == True
        )
    )
    presentation = result.scalars().first()
    
    if not presentation:
        return HTMLResponse("""
        <html>
            <head><title>Презентация не найдена</title></head>
            <body>
                <h1>❌ Презентация не найдена</h1>
                <p>Публичная презентация не существует или была удалена.</p>
            </body>
        </html>
        """, status_code=404)
    
    # Генерируем HTML для просмотра
    slides_html = ""
    for i, slide in enumerate(presentation.content.get("slides", [])):
        slides_html += f"""
        <div class="slide" id="slide-{i}" style="display: {'block' if i == 0 else 'none'}">
            <h2>{slide.get('title', '')}</h2>
            <div class="content">{slide.get('content', '').replace(chr(10), '<br>')}</div>
        </div>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{presentation.title} - SayDeck</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }}
            .presentation-container {{
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid rgba(255, 255, 255, 0.2);
                padding-bottom: 20px;
            }}
            .slide {{
                background: rgba(255, 255, 255, 0.05);
                padding: 30px;
                border-radius: 15px;
                margin: 20px 0;
                min-height: 400px;
            }}
            .slide h2 {{
                color: #fff;
                margin-top: 0;
                font-size: 2em;
                margin-bottom: 20px;
            }}
            .content {{
                font-size: 1.2em;
                line-height: 1.6;
                color: rgba(255, 255, 255, 0.9);
            }}
            .controls {{
                text-align: center;
                margin-top: 30px;
            }}
            button {{
                background: #28a745;
                color: white;
                border: none;
                padding: 12px 24px;
                margin: 0 10px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                transition: background 0.3s;
            }}
            button:hover {{
                background: #218838;
            }}
            button:disabled {{
                background: #6c757d;
                cursor: not-allowed;
            }}
            .slide-counter {{
                background: rgba(0, 0, 0, 0.3);
                padding: 8px 15px;
                border-radius: 20px;
                margin: 20px 0;
                text-align: center;
            }}
            .share-info {{
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                text-align: center;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="presentation-container">
            <div class="header">
                <h1>🎤 {presentation.title}</h1>
                <p>Публичная презентация из SayDeck</p>
                <div class="slide-counter">
                    <span id="current-slide">1</span> / <span id="total-slides">{len(presentation.content.get('slides', []))}</span>
                </div>
            </div>
            
            <div class="slides-container">
                {slides_html}
            </div>
            
            <div class="controls">
                <button id="prev-btn" onclick="prevSlide()">← Предыдущий</button>
                <button id="next-btn" onclick="nextSlide()">Следующий →</button>
            </div>
            
            <div class="share-info">
                <p>💡 Создано в <strong>SayDeck</strong> - генерация презентаций с помощью AI</p>
                <p>🔗 Поделиться: <code>{public_id}</code></p>
            </div>
        </div>

        <script>
            let currentSlide = 0;
            const totalSlides = {len(presentation.content.get('slides', []))};
            
            function showSlide(n) {{
                const slides = document.querySelectorAll('.slide');
                slides.forEach(slide => slide.style.display = 'none');
                
                if (n >= totalSlides) currentSlide = 0;
                if (n < 0) currentSlide = totalSlides - 1;
                
                slides[currentSlide].style.display = 'block';
                document.getElementById('current-slide').textContent = currentSlide + 1;
                
                // Обновляем кнопки
                document.getElementById('prev-btn').disabled = currentSlide === 0;
                document.getElementById('next-btn').disabled = currentSlide === totalSlides - 1;
            }}
            
            function nextSlide() {{
                if (currentSlide < totalSlides - 1) {{
                    currentSlide++;
                    showSlide(currentSlide);
                }}
            }}
            
            function prevSlide() {{
                if (currentSlide > 0) {{
                    currentSlide--;
                    showSlide(currentSlide);
                }}
            }}
            
            // Управление клавиатурой
            document.addEventListener('keydown', function(e) {{
                if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
                if (e.key === 'ArrowLeft') prevSlide();
            }});
            
            // Инициализация
            showSlide(0);
        </script>
    </body>
    </html>
    """
    
    # Увеличиваем счетчик просмотров
    await session.execute(
        update(Presentation)
        .where(Presentation.id == presentation.id)
        .values(views_count=(Presentation.views_count or 0) + 1)
    )
    await session.commit()
    
    return HTMLResponse(html_content)

@router.get("/presentations")
async def list_public_presentations(
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_session)
):
    """Список всех публичных презентаций"""
    
    result = await session.execute(
        select(Presentation)
        .where(Presentation.is_public == True)
        .order_by(Presentation.views_count.desc())
        .limit(limit)
        .offset(offset)
    )
    presentations = result.scalars().all()
    
    return {
        "presentations": [
            {
                "id": p.id,
                "title": p.title,
                "public_id": p.public_id,
                "views_count": p.views_count or 0,
                "created_at": p.created_at,
                "slides_count": len(p.content.get("slides", [])),
                "preview_url": f"/public/presentations/{p.public_id}/viewer"
            }
            for p in presentations
        ],
        "total": len(presentations),
        "limit": limit,
        "offset": offset
    }
