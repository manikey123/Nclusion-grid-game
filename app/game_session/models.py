from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database import Base
from app.game_session.schemas import GameResult, GameSessionStatus

class GameSession(Base):
    __tablename__ = "game_session"
    
    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String(36), unique=True, index=True, nullable=False)

    # Status by default is WAITING until second player joins
    status = Column(Enum(GameSessionStatus), default=GameSessionStatus.WAITING, nullable=False)

    # The idea here is to maintain the game state on the server side so there won't be inconsistencies
    # in game state or move between the clients. 
    # Holding state in client cache may work but not a stable model to follow
    #
    # Defaulting to 0's as we won't have any moves at first
    game_state = Column(JSON, default=lambda: [[0,0,0],[0,0,0],[0,0,0]], nullable=False)

    current_turn_player_id = Column(Integer, ForeignKey("player.id"))
    winner_id = Column(Integer, ForeignKey("player.id"))
    game_result = Column(Enum(GameResult))

    player1_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("player.id"))

    created_at = Column(DateTime, server_default=func.now())
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    
    # Relationships
    player1 = relationship("Player", foreign_keys=[player1_id])
    player2 = relationship("Player", foreign_keys=[player2_id])

    current_turn_player = relationship("Player", foreign_keys=[current_turn_player_id])
    winner = relationship("Player", foreign_keys=[winner_id])
