from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.player.schemas import PlayerCreate, PlayerResponse
from app.player.service import PlayerService

router = APIRouter()
player_service = PlayerService()

@router.post("/", response_model=PlayerResponse)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    # Check if username exists
    existing = player_service.get_player_by_username(db, player.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email exists
    existing_email = player_service.get_player_by_email(db, player.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    return player_service.create_player(db, player)


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = player_service.get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player