from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class JungleTimer(Base):
    __tablename__ = "jungle_timers"
    
    id = Column(Integer, primary_key=True, index=True)
    game_session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    objective_type = Column(String, nullable=False)  # dragon, baron, herald, gromp, krugs, etc.
    objective_name = Column(String, nullable=False)  # specific name like "Ocean Dragon"
    spawn_time = Column(DateTime(timezone=True), nullable=False)
    respawn_time = Column(DateTime(timezone=True), nullable=True)
    is_secured = Column(Boolean, default=False)
    secured_by_team = Column(String, nullable=True)  # "blue" or "red"
    game_time_minutes = Column(Integer, nullable=False)  # game time when objective spawns
    is_active = Column(Boolean, default=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    game_session = relationship("GameSession", backref="jungle_timers")
    
    def __repr__(self):
        return f"<JungleTimer(objective='{self.objective_name}', spawn_time='{self.spawn_time}')>" 