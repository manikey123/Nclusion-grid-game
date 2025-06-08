from pydantic import BaseModel
from datetime import datetime

class PlayerCreate(BaseModel):
    username: str
    email: str

class PlayerResponse(BaseModel):
    id: int
    username: str
    email: str
    total_games: int
    total_wins: int
    win_rate: float
    created_at: datetime

    class ConfigDict:
        from_attributes = True