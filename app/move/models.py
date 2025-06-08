from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class Move(Base):
    __tablename__ = "move"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("game_session.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    row_position = Column(Integer, nullable=False)
    col_position = Column(Integer, nullable=False)