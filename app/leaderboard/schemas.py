from pydantic import BaseModel
from typing import List, Optional

class LeaderboardPlayer(BaseModel):
    id: int
    username: str
    total_wins: int
    efficiency: Optional[float] = None  

    class ConfigDict:
        from_attributes = True

class LeaderboardResponse(BaseModel):
    players: List[LeaderboardPlayer]
    ranking_type: str 