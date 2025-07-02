from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from models.base import get_session
from models.template import Template
from schemas.template import TemplateResponse
from sqlalchemy import select

router = APIRouter(prefix="/templates", tags=["templates"])

@router.get("/", response_model=List[TemplateResponse])
async def get_templates(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Template))
    templates = result.scalars().all()
    return templates

@router.get("/popular", response_model=List[TemplateResponse])
async def get_popular_templates(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Template).where(Template.is_popular == True))
    templates = result.scalars().all()
    return templates

@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Template).where(Template.id == template_id))
    template = result.scalars().first()
    if not template:
        raise HTTPException(status_code=404, detail="Шаблон не найден")
    return template 