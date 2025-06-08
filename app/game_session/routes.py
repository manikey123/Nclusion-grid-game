# app/game_session/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.game_session.service import GameSessionService
from app.player.service import PlayerService
from app.game_session.schemas import (
    CreateGameSessionRequest,
    JoinGameSessionRequest,
    GameSessionCreateResponse,
    GameSessionJoinResponse,
    GameSessionResponse
)

router = APIRouter()
game_session_service = GameSessionService()
player_service = PlayerService()

@router.post("/create", response_model=GameSessionCreateResponse)
def create_session(request: CreateGameSessionRequest, db: Session = Depends(get_db)):
    # Validate player exists
    player = player_service.get_player(db, request.player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    game_session = game_session_service.create_game_session(db, request.player_id)
    
    return GameSessionCreateResponse(
        session_id=game_session.id,
        session_code=game_session.session_code,
        status=game_session.status
    )

@router.post("/join/{session_code}", response_model=GameSessionJoinResponse)
def join_game_session(session_code: str, request: JoinGameSessionRequest, db: Session = Depends(get_db)):
    # Validate player exists
    player = player_service.get_player(db, request.player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    try:
        session = game_session_service.join_game_session(db, session_code, request.player_id)
        
        return GameSessionJoinResponse(
            session_id=session.id,
            status=session.status,
            game_started=True,
            player1_id=session.player1_id,
            player2_id=session.player2_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{session_id}", response_model=GameSessionResponse)
def get_game_session(session_id: int, db: Session = Depends(get_db)):
    session = game_session_service.get_game_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return GameSessionResponse(
        id=session.id,
        session_code=session.session_code,
        status=session.status,
        game_state=session.game_state,
        current_turn_player_id=session.current_turn_player_id,
        winner_id=session.winner_id,
        player1_id=session.player1_id,
        player2_id=session.player2_id
    )