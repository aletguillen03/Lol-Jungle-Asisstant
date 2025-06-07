from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    riot_id = Column(String, unique=True, index=True, nullable=False)
    summoner_name = Column(String, index=True, nullable=False)
    tag_line = Column(String, nullable=False)
    region = Column(String, nullable=False, default="americas")
    rank_tier = Column(String, nullable=True)
    rank_division = Column(String, nullable=True)
    league_points = Column(Integer, default=0)
    preferred_jungle_champions = Column(String, nullable=True)  # JSON string
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(riot_id='{self.riot_id}', summoner_name='{self.summoner_name}')>" 