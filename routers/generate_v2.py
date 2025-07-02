"""
Новый роутер для генерации с поддержкой множественных AI провайдеров
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import aiofiles
import os
from models.base import get_session
from models.user import User
from models.presentation import Presentation
from schemas.presentation import PresentationResponse
from utils.auth import get_current_user
from config.settings import get_settings
from ai_services import ai_manager, AIProviderType, AIGenerationRequest, AITranscriptionRequest

router = APIRouter(prefix="/generate", tags=["generate"])
settings = get_settings()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/providers")
async def get_available_providers():
    """Получить список доступных AI провайдеров"""
    return {
        "providers": ai_manager.get_available_providers(),
        "default_provider": ai_manager.default_provider.value
    }

@router.post("/text", response_model=PresentationResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def generate_from_text(
    text: str = Body(..., description="Текст для создания презентации"),
    language: str = Body("ru", description="Язык презентации"),
    animation: bool = Body(False, description="Включить анимации"),
    slides_count: int = Body(5, description="Количество слайдов"),
    provider: Optional[str] = Body(None, description="AI провайдер (openai, groq, ollama)"),
    template: Optional[str] = Body(None, description="Шаблон презентации"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Генерация презентации из текста с выбором AI провайдера"""
    
    # Определяем провайдера
    provider_type = None
    if provider:
        try:
            provider_type = AIProviderType(provider.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Неподдерживаемый провайдер: {provider}. Доступные: openai, groq, ollama"
            )
    
    # Создаем запрос
    request = AIGenerationRequest(
        text=text,
        language=language,
        slides_count=slides_count,
        animation=animation,
        template=template
    )
    
    try:
        # Генерируем презентацию
        presentation_data = await ai_manager.generate_presentation(request, provider_type)
        
        # Сохраняем в базу
        new_presentation = Presentation(
            title=presentation_data.get("title", "Новая презентация"),
            content=presentation_data,
            user_id=current_user.id
        )
        session.add(new_presentation)
        await session.commit()
        await session.refresh(new_presentation)
        
        return new_presentation
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка генерации: {str(e)}"
        )

@router.post("/audio", response_model=PresentationResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def generate_from_audio(
    audio_file: UploadFile = File(..., description="Аудио файл для транскрипции"),
    language: str = Body("ru", description="Язык аудио"),
    animation: bool = Body(False, description="Включить анимации"),
    slides_count: int = Body(5, description="Количество слайдов"),
    provider: Optional[str] = Body(None, description="AI провайдер для генерации"),
    transcription_provider: Optional[str] = Body(None, description="AI провайдер для транскрипции"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Генерация презентации из аудио файла"""
    
    # Проверяем размер файла
    if audio_file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл слишком большой"
        )
    
    # Сохраняем файл
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{audio_file.filename}")
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await audio_file.read()
        await out_file.write(content)
    
    try:
        # Определяем провайдеров
        transcription_provider_type = None
        if transcription_provider:
            try:
                transcription_provider_type = AIProviderType(transcription_provider.lower())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Неподдерживаемый провайдер транскрипции: {transcription_provider}"
                )
        
        generation_provider_type = None
        if provider:
            try:
                generation_provider_type = AIProviderType(provider.lower())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Неподдерживаемый провайдер генерации: {provider}"
                )
        
        # Транскрибируем аудио
        transcription_request = AITranscriptionRequest(
            audio_file_path=file_path,
            language=language
        )
        text = await ai_manager.transcribe_audio(transcription_request, transcription_provider_type)
        
        # Генерируем презентацию
        generation_request = AIGenerationRequest(
            text=text,
            language=language,
            slides_count=slides_count,
            animation=animation
        )
        presentation_data = await ai_manager.generate_presentation(generation_request, generation_provider_type)
        
        # Добавляем информацию о транскрипции
        presentation_data["_transcription"] = {
            "original_text": text,
            "audio_filename": audio_file.filename
        }
        
        # Сохраняем в базу
        new_presentation = Presentation(
            title=presentation_data.get("title", "Презентация из аудио"),
            content=presentation_data,
            user_id=current_user.id
        )
        session.add(new_presentation)
        await session.commit()
        await session.refresh(new_presentation)
        
        return new_presentation
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка обработки аудио: {str(e)}"
        )
    finally:
        # Удаляем временный файл
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/batch", response_model=List[PresentationResponse])
async def generate_batch_presentations(
    texts: List[str] = Body(..., description="Список текстов для генерации"),
    language: str = Body("ru", description="Язык презентаций"),
    slides_count: int = Body(3, description="Количество слайдов в каждой"),
    provider: Optional[str] = Body(None, description="AI провайдер"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Массовая генерация презентаций"""
    
    if len(texts) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Максимум 10 презентаций за раз"
        )
    
    provider_type = None
    if provider:
        try:
            provider_type = AIProviderType(provider.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Неподдерживаемый провайдер: {provider}"
            )
    
    results = []
    for i, text in enumerate(texts):
        try:
            request = AIGenerationRequest(
                text=text,
                language=language,
                slides_count=slides_count,
                animation=False
            )
            
            presentation_data = await ai_manager.generate_presentation(request, provider_type)
            
            new_presentation = Presentation(
                title=presentation_data.get("title", f"Презентация {i+1}"),
                content=presentation_data,
                user_id=current_user.id
            )
            session.add(new_presentation)
            results.append(new_presentation)
            
        except Exception as e:
            print(f"Error generating presentation {i+1}: {e}")
            continue
    
    await session.commit()
    
    # Обновляем объекты
    for presentation in results:
        await session.refresh(presentation)
    
    return results

@router.post("/test/all")
async def test_all_providers():
    """Тестирование всех AI провайдеров"""
    test_request = AIGenerationRequest(
        text="Тестовый текст для проверки работы AI провайдеров",
        language="ru",
        slides_count=2
    )
    
    results = {}
    for provider_type in AIProviderType:
        try:
            provider = ai_manager.get_provider(provider_type)
            if provider.is_available():
                result = await provider.generate_presentation(test_request)
                results[provider_type.value] = {
                    "status": "success",
                    "provider_name": provider.get_provider_name(),
                    "title": result.get("title", "No title"),
                    "slides_count": len(result.get("slides", []))
                }
            else:
                results[provider_type.value] = {
                    "status": "unavailable",
                    "provider_name": provider.get_provider_name()
                }
        except Exception as e:
            results[provider_type.value] = {
                "status": "error",
                "error": str(e)
            }
    
    return results

@router.post("/test/groq")
async def test_groq_directly():
    """Прямой тест Groq провайдера для отладки"""
    try:
        from ai_services.groq_provider import GroqProvider
        
        # Создаем провайдера напрямую
        provider = GroqProvider()
        
        if not provider.is_available():
            return {
                "status": "error",
                "message": "Groq провайдер недоступен - проверьте API ключ"
            }
        
        # Тестовый запрос
        test_request = AIGenerationRequest(
            text="Искусственный интеллект в образовании: преимущества и вызовы современной эпохи цифровизации",
            language="ru",
            slides_count=4,
            animation=False
        )
        
        # Генерируем презентацию
        result = await provider.generate_presentation(test_request)
        
        return {
            "status": "success",
            "provider": provider.get_provider_name(),
            "result": result
        }
        
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }
