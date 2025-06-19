from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles
import os
from models.base import get_session
from models.user import User
from models.presentation import Presentation
from schemas.presentation import PresentationResponse
from utils.auth import get_current_user
from utils.openai_client import transcribe_audio, generate_presentation_structure
from config.settings import get_settings

router = APIRouter(prefix="/generate", tags=["generate"])
settings = get_settings()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/audio", response_model=PresentationResponse)
async def generate_from_audio(
    audio_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    # Проверяем размер файла
    if audio_file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large"
        )
    
    # Сохраняем файл
    file_path = os.path.join(UPLOAD_DIR, audio_file.filename)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await audio_file.read()
        await out_file.write(content)
    
    try:
        # Транскрибируем аудио
        text = await transcribe_audio(file_path)
        
        # Генерируем структуру презентации
        presentation_data = await generate_presentation_structure(text)
        
        # Создаем презентацию
        new_presentation = Presentation(
            title=presentation_data["title"],
            content=presentation_data,
            user_id=current_user.id
        )
        session.add(new_presentation)
        await session.commit()
        await session.refresh(new_presentation)
        
        return new_presentation
    
    finally:
        # Удаляем временный файл
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/text", response_model=PresentationResponse)
async def generate_from_text(
    text: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    # Генерируем структуру презентации
    presentation_data = await generate_presentation_structure(text)
    
    # Создаем презентацию
    new_presentation = Presentation(
        title=presentation_data["title"],
        content=presentation_data,
        user_id=current_user.id
    )
    session.add(new_presentation)
    await session.commit()
    await session.refresh(new_presentation)
    
    return new_presentation 