from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from models.base import get_session
from models.user import User
from models.presentation import Presentation
from schemas.presentation import PresentationResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/presentations", tags=["presentations"])

@router.get("/", response_model=List[PresentationResponse])
async def get_presentations(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    presentations = await session.query(Presentation).filter(
        Presentation.user_id == current_user.id
    ).all()
    return presentations

@router.get("/{presentation_id}", response_model=PresentationResponse)
async def get_presentation(
    presentation_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    presentation = await session.query(Presentation).filter(
        Presentation.id == presentation_id,
        Presentation.user_id == current_user.id
    ).first()
    
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presentation not found"
        )
    
    return presentation 