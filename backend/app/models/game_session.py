from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class GameSession(Base):
    __tablename__ = "game_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    match_id = Column(String, unique=True, index=True, nullable=False)
    champion_name = Column(String, nullable=False)
    game_mode = Column(String, nullable=False, default="CLASSIC")
    game_duration = Column(Integer, nullable=True)  # in seconds
    won = Column(Boolean, nullable=True)
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    cs_score = Column(Integer, default=0)
    jungle_cs = Column(Integer, default=0)
    vision_score = Column(Integer, default=0)
    objectives_secured = Column(Text, nullable=True)  # JSON string
    ai_suggestions = Column(Text, nullable=True)  # JSON string of AI suggestions
    notes = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", backref="game_sessions") 
    
    def __repr__(self):
        return f"<GameSession(match_id='{self.match_id}', champion='{self.champion_name}')>" 