from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from models.base import get_session
from models.user import User
from models.presentation import Presentation
from schemas.presentation import PresentationResponse, PresentationCreate
from utils.auth import get_current_user

import os
from sqlalchemy import select

# Import PPTX generator
from utils.pptx_generator import generate_presentation_pptx

router = APIRouter(prefix="/presentations", tags=["presentations"])

@router.get("/", response_model=List[PresentationResponse])
async def get_presentations(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    stmt = select(Presentation).where(Presentation.user_id == current_user.id)
    result = await session.execute(stmt)
    presentations = result.scalars().all()
    return presentations

@router.get("/{presentation_id}", response_model=PresentationResponse)
async def get_presentation(
    presentation_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    stmt = select(Presentation).where(
        (Presentation.id == presentation_id) & 
        (Presentation.user_id == current_user.id)
    )
    result = await session.execute(stmt)
    presentation = result.scalars().first()
    
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presentation not found"
        )
    
    return presentation 

@router.post("/", response_model=PresentationResponse)
async def create_presentation(
    presentation: PresentationCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    user_role = current_user.role  # str
    user_credits = current_user.credits  # int
    
    if user_role == "guest":
        if user_credits <= 0:
            raise HTTPException(status_code=403, detail="Кредиты закончились")
        if len(presentation.content.get("slides", [])) > 5:
            raise HTTPException(status_code=403, detail="Гостям доступно не более 5 слайдов")
        raise HTTPException(status_code=403, detail="Гостям нельзя сохранять презентации")
    
    
    new_presentation = Presentation(
        user_id=current_user.id,
        board_id=presentation.board_id
    )
    new_presentation.title = presentation.title
    new_presentation.content = presentation.content
    
    session.add(new_presentation)
    await session.commit()
    await session.refresh(new_presentation)
    return new_presentation

@router.put("/{presentation_id}", response_model=PresentationResponse)
async def update_presentation(
    presentation_id: int,
    presentation: PresentationCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    stmt = select(Presentation).where(
        (Presentation.id == presentation_id) & 
        (Presentation.user_id == current_user.id)
    )
    result = await session.execute(stmt)
    db_presentation = result.scalars().first()
    if not db_presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")
    db_presentation.title = presentation.title
    db_presentation.content = presentation.content
    db_presentation.board_id = presentation.board_id
    await session.commit()
    await session.refresh(db_presentation)
    return db_presentation

@router.delete("/{presentation_id}")
async def delete_presentation(
    presentation_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    stmt = select(Presentation).where(
        (Presentation.id == presentation_id) & 
        (Presentation.user_id == current_user.id)
    )
    result = await session.execute(stmt)
    db_presentation = result.scalars().first()
    if not db_presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")
    await session.delete(db_presentation)
    await session.commit()
    return {"ok": True}

@router.get("/download/{presentation_id}")
async def download_presentation(
    presentation_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Presentation).where(Presentation.id == presentation_id, Presentation.user_id == current_user.id))
    db_presentation = result.scalars().first()
    if not db_presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")
    
    try:
        # Генерируем PPTX файл
        pptx_path = await generate_presentation_pptx(db_presentation.content)
        return FileResponse(
            pptx_path, 
            filename=f"presentation_{presentation_id}.pptx",
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    except Exception as e:
        # В случае ошибки возвращаем JSON с данными презентации
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PPTX: {str(e)}"
        ) 