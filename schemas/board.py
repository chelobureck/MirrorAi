from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BoardCreate(BaseModel):
    name: str

class BoardResponse(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 