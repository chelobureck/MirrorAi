"""
Templates Router - публичные эндпоинты для работы с шаблонами презентаций
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from models.base import get_session
from models.user import User
from utils.auth import get_current_user
from services.template_service import template_service, TemplateService
from schemas.template import (
    TemplateResponse, 
    TemplateDetail, 
    TemplateCreateResponse, 
    TemplateDeleteResponse
)

router = APIRouter(prefix="/api/v1/templates", tags=["templates"])

@router.post("/{presentation_id}/save", response_model=TemplateCreateResponse)
async def save_presentation_as_template(
    presentation_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Сохраняет существующую презентацию (по ID) как шаблон"""
    try:
        result = await template_service.create_template_from_presentation(
            presentation_id=presentation_id,
            user_id=current_user.id,
            session=session
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating template: {str(e)}"
        )

@router.delete("/{template_id}", response_model=TemplateDeleteResponse)
async def delete_template(
    template_id: str,  # public_id
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Удаляет шаблон по публичному ID"""
    try:
        result = await template_service.delete_template(
            public_id=template_id,
            user_id=current_user.id,
            session=session
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting template: {str(e)}"
        )

@router.get("/{template_id}", response_model=TemplateDetail)
async def get_template(
    template_id: str,  # public_id
    session: AsyncSession = Depends(get_session)
):
    """Возвращает данные шаблона по публичному ID"""
    template = await template_service.get_template_by_public_id(
        public_id=template_id,
        session=session
    )
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return template

@router.get("/{template_id}/viewer", response_class=HTMLResponse)
async def get_template_viewer(
    template_id: str,  # public_id
    session: AsyncSession = Depends(get_session)
):
    """Возвращает HTML шаблона для предпросмотра"""
    html_content = await template_service.get_template_html(
        public_id=template_id,
        session=session
    )
    
    if not html_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return HTMLResponse(
        content=html_content,
        status_code=200,
        headers={"Content-Type": "text/html; charset=utf-8"}
    )

@router.get("/", response_model=List[TemplateResponse])
async def list_templates(
    session: AsyncSession = Depends(get_session)
):
    """Список всех доступных шаблонов"""
    templates = await template_service.list_all_templates(session=session)
    return templates

@router.get("/builtin", response_class=JSONResponse)
async def list_builtin_templates():
    """Список всех встроенных шаблонов (статичные)"""
    return TemplateService.list_builtin_templates()

@router.get("/builtin/{template_id}", response_class=JSONResponse)
async def get_builtin_template(template_id: str):
    """Получить встроенный шаблон по ID (статичный)"""
    template = TemplateService.get_builtin_template(template_id)
    if not template:
        return JSONResponse(status_code=404, content={"detail": "Template not found"})
    return template