from pydantic import BaseModel, field_validator
from typing import Optional, List

class CreateMoveRequest(BaseModel):
    session_id: int
    player_id: int
    row: int
    col: int
    
    @field_validator('row', 'col')
    @classmethod
    def validate_position(cls, v):
        if not (0 <= v <= 2):
            raise ValueError('Position must be between 0 and 2 (inclusive)')
        return v

class MoveResponse(BaseModel):
    id: int
    session_id: int
    player_id: int
    row_position: int
    col_position: int

    class ConfigDict:
        from_attributes = True

class CreateMoveResponse(BaseModel):
    id: int
    session_id: int
    game_state: List[List[int]]
    game_status: str
    winner_id: Optional[int]
    current_turn_player_id: Optional[int]

class SessionMovesResponse(BaseModel):
    session_id: int
    total_moves: int
    moves: List[MoveResponse]