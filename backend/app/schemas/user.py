from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    riot_id: str
    summoner_name: str
    tag_line: str
    region: str = "americas"
    rank_tier: Optional[str] = None
    rank_division: Optional[str] = None
    league_points: int = 0
    preferred_jungle_champions: Optional[str] = None  # JSON string

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    summoner_name: Optional[str] = None
    tag_line: Optional[str] = None
    region: Optional[str] = None
    rank_tier: Optional[str] = None
    rank_division: Optional[str] = None
    league_points: Optional[int] = None
    preferred_jungle_champions: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True) 