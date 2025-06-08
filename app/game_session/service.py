from sqlalchemy.orm import Session
from app.game_session.models import GameSession, GameSessionStatus
from datetime import datetime, timezone
import uuid

class GameSessionService:
    def create_game_session(self, db: Session, player_id: int) -> GameSession:
        session = GameSession(
            session_code=str(uuid.uuid4()),
            player1_id=player_id,
            current_turn_player_id=player_id,
            status=GameSessionStatus.WAITING
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    def join_game_session(self, db: Session, session_code: str, player_id: int) -> GameSession:
        game_session = db.query(GameSession).filter(
            GameSession.session_code == session_code,
            GameSession.status == GameSessionStatus.WAITING
        ).first()
        
        if not game_session:
            raise ValueError("Session not found or not available")
        
        if game_session.player1_id == player_id:
            raise ValueError("Cannot join your own session")
            
        # Join as player 2 and start game
        game_session.player2_id = player_id
        game_session.status = GameSessionStatus.ACTIVE
        game_session.started_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(game_session)
        return game_session
    
    def get_game_session(self, db: Session, session_id: int) -> GameSession:
        return db.query(GameSession).filter(GameSession.id == session_id).first()
    
    def get_game_session_by_code(self, db: Session, session_code: str) -> GameSession:
        return db.query(GameSession).filter(GameSession.session_code == session_code).first()