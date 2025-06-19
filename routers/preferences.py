from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import get_session
from models.user import User
from models.userpreferences import UserPreferences
from schemas.userpreferences import UserPreferencesResponse, UserPreferencesUpdate
from utils.auth import get_current_user

router = APIRouter(prefix="/user/preferences", tags=["user-preferences"])

@router.get("/", response_model=UserPreferencesResponse)
async def get_preferences(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    prefs = await session.query(UserPreferences).filter(UserPreferences.id == current_user.preferences_id).first()
    if not prefs:
        raise HTTPException(status_code=404, detail="Настройки не найдены")
    return prefs

@router.patch("/", response_model=UserPreferencesResponse)
async def update_preferences(
    update: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    prefs = await session.query(UserPreferences).filter(UserPreferences.id == current_user.preferences_id).first()
    if not prefs:
        raise HTTPException(status_code=404, detail="Настройки не найдены")
    for field, value in update.dict(exclude_unset=True).items():
        setattr(prefs, field, value)
    await session.commit()
    await session.refresh(prefs)
    return prefs 