from sqlalchemy.orm import Session
from app.player.models import Player
from app.player.schemas import PlayerCreate

class PlayerService:
    def create_player(self, db: Session, player_data: PlayerCreate) -> Player:
        player = Player(**player_data.model_dump())
        db.add(player)
        db.commit()
        db.refresh(player)
        return player
    
    def get_player(self, db: Session, player_id: int) -> Player:
        return db.query(Player).filter(Player.id == player_id).first()
    
    def get_player_by_username(self, db: Session, username: str) -> Player:
        return db.query(Player).filter(Player.username == username).first()
    
    def get_player_by_email(self, db: Session, email: str) -> Player:
        return db.query(Player).filter(Player.email == email).first()
    