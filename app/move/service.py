from sqlalchemy.orm import Session
from app.move.models import Move

class MoveService:
    def create_move(self, db: Session, session_id: int, player_id: int, row: int, col: int) -> Move:
        move = Move(
            session_id=session_id,
            player_id=player_id,
            row_position=row,
            col_position=col
        )
        db.add(move)
        db.commit()
        db.refresh(move)
        
        return move
    
    def get_moves_for_game_session(self, db: Session, session_id: int):
        return db.query(Move).filter(Move.session_id == session_id).all()
    
    def get_move_for_game_session(self, db: Session, session_id: int):
        return db.query(Move).filter(Move.session_id == session_id).first()