from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body
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

@router.post("/url", response_model=PresentationResponse)
async def generate_from_url(
    url: str = Body(...),
    language: str = Body("ru"),
    animation: bool = Body(False),
    slides_count: int = Body(5),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    # Здесь должна быть логика получения текста по url (заглушка)
    text = f"Контент с {url} (заглушка)"
    presentation_data = await generate_presentation_structure(text, language=language, animation=animation, slides_count=slides_count)
    new_presentation = Presentation(
        title=presentation_data["title"],
        content=presentation_data,
        user_id=current_user.id
    )
    session.add(new_presentation)
    await session.commit()
    await session.refresh(new_presentation)
    return new_presentation

@router.post("/audio", response_model=PresentationResponse)
async def generate_from_audio(
    audio_file: UploadFile = File(...),
    language: str = Body("ru"),
    animation: bool = Body(False),
    slides_count: int = Body(5),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if audio_file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large"
        )
    file_path = os.path.join(UPLOAD_DIR, audio_file.filename)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await audio_file.read()
        await out_file.write(content)
    try:
        text = await transcribe_audio(file_path)
        presentation_data = await generate_presentation_structure(text, language=language, animation=animation, slides_count=slides_count)
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
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/text", response_model=PresentationResponse)
async def generate_from_text(
    text: str = Body(...),
    language: str = Body("ru"),
    animation: bool = Body(False),
    slides_count: int = Body(5),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    presentation_data = await generate_presentation_structure(text, language=language, animation=animation, slides_count=slides_count)
    new_presentation = Presentation(
        title=presentation_data["title"],
        content=presentation_data,
        user_id=current_user.id
    )
    session.add(new_presentation)
    await session.commit()
    await session.refresh(new_presentation)
    return new_presentation 