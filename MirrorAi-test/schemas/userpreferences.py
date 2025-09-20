from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class UserPreferencesBase(BaseModel):
    default_theme: Optional[str] = "modern"
    default_slide_count: Optional[int] = 10
    preferred_ai_provider: Optional[str] = "groq"
    preferences: Optional[Dict[str, Any]] = None

class UserPreferencesCreate(UserPreferencesBase):
    pass

class UserPreferencesUpdate(BaseModel):
    default_theme: Optional[str] = None
    default_slide_count: Optional[int] = None
    preferred_ai_provider: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

class UserPreferencesResponse(UserPreferencesBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
