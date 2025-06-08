from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class GameSessionStatus(str, Enum):
    WAITING = "WAITING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"

# We are only tracking wins and draws
# If a win, then either Player 1 wins or Player 2 wins 
# so no need to track LOSS
class GameResult(str, Enum):
    WIN = "WIN"
    DRAW = "DRAW"

class CreateGameSessionRequest(BaseModel):
    player_id: int

class JoinGameSessionRequest(BaseModel):
    player_id: int

class GameSessionCreateResponse(BaseModel):
    session_id: int
    session_code: str
    status: GameSessionStatus

class GameSessionJoinResponse(BaseModel):
    session_id: int
    status: GameSessionStatus
    game_started: bool
    player1_id: int
    player2_id: int

class GameSessionResponse(BaseModel):
    id: int
    session_code: str
    status: GameSessionStatus
    game_state: List[List[int]]
    current_turn_player_id: Optional[int]
    winner_id: Optional[int]
    player1_id: int
    player2_id: Optional[int]

    class ConfigDict:
        from_attributes = True

class GameSessionDetailResponse(BaseModel):
    id: int
    session_code: str
    status: GameSessionStatus
    game_state: List[List[int]]
    current_turn_player_id: Optional[int]
    winner_id: Optional[int]
    game_result: Optional[GameResult]
    created_at: datetime
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    player1_id: int
    player2_id: Optional[int]

    class ConfigDict:
        from_attributes = True