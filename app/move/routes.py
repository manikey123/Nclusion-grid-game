from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.game_session.schemas import GameSessionStatus
from app.game_session.service import GameSessionService
from app.leaderboard.service import LeaderboardService
from app.core.engine import GameEngine
from app.move.service import MoveService
from app.move.schemas import (
    CreateMoveRequest,
    CreateMoveResponse,
    MoveResponse,
    SessionMovesResponse
)


router = APIRouter()
game_session_service = GameSessionService()
move_service = MoveService()
leader_board_service = LeaderboardService()

@router.post("/", response_model=CreateMoveResponse)
def make_move(request: CreateMoveRequest, db: Session = Depends(get_db)):
    
    session = game_session_service.get_game_session(db, request.session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    success = GameEngine.make_move(session, request.player_id, request.row, request.col)

    if not success:
        if session.status.value != "ACTIVE":
            error_msg = f"Game is not active (status: {session.status.value})"
        elif session.current_turn_player_id != request.player_id:
            error_msg = "Not your turn"
        elif not (0 <= request.row <= 2 and 0 <= request.col <= 2):
            error_msg = "Position out of bounds"
        elif session.game_state[request.row][request.col] != 0:
            error_msg = "Cell already occupied"
        else:
            error_msg = "Invalid move"
            
        raise HTTPException(status_code=400, detail=error_msg)

    move = move_service.create_move(
        db, request.session_id, request.player_id, request.row, request.col
    )
    if(session.status == GameSessionStatus.COMPLETED):
        leader_board_service.update_player_stats(db, session.winner_id)
    
    return CreateMoveResponse(
        id=move.id,
        session_id = session.id,
        game_state=session.game_state,
        game_status=session.status.value,
        winner_id=session.winner_id,
        current_turn_player_id=session.current_turn_player_id
    )

@router.get("/session/{session_id}", response_model=SessionMovesResponse)
def get_session_moves(session_id: int, db: Session = Depends(get_db)):

    session = game_session_service.get_game_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    moves = move_service.get_moves_for_game_session(db, session_id)
    # We need to convert the move to moveResponse object
    move_responses = [
        MoveResponse(
            id=move.id,
            session_id=move.session_id,
            player_id=move.player_id,
            row_position=move.row_position,
            col_position=move.col_position
        )
        for move in moves
    ]
    return SessionMovesResponse(
        session_id=session_id,
        total_moves=len(moves),
        moves=move_responses  
    )

@router.get("/{move_id}", response_model=MoveResponse)
def get_move(move_id: int, db: Session = Depends(get_db)):
    
    move = move_service.get_move_for_game_session(db, move_id)
    if not move:
        raise HTTPException(status_code=404, detail="Move not found")
    # We need to convert the move to moveResponse object
    move_response = MoveResponse(
            id=move.id,
            session_id=move.session_id,
            player_id=move.player_id,
            row_position=move.row_position,
            col_position=move.col_position
        )
    return move_response 