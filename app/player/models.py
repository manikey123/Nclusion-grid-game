from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base

class Player(Base):
    __tablename__ = "player"
    
    id = Column(Integer, primary_key=True, index=True)
    # Display name for player
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    # Tracking leaderboard performance
    total_games = Column(Integer, default=0)
    # Tracking leaderboard ranking
    total_wins = Column(Integer, default=0)
    # Track player efficiency
    win_rate = Column(Float, default=0.0)