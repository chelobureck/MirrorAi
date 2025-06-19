from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class PresentationBase(BaseModel):
    title: str

class PresentationCreate(PresentationBase):
    content: Dict[str, Any]

class PresentationResponse(PresentationBase):
    id: int
    user_id: int
    content: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 