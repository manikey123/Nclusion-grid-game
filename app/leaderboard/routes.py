from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.leaderboard.service import LeaderboardService
from app.leaderboard.schemas import LeaderboardResponse, LeaderboardPlayer

router = APIRouter()
leaderboard_service = LeaderboardService()

@router.get("/wins", response_model=LeaderboardResponse)
def get_leaderboard_by_wins(db: Session = Depends(get_db)):
    """Get top 3 players by wins."""
    players = leaderboard_service.get_top_players_by_wins(db, 3)
    
    player_entries = [
        LeaderboardPlayer(
            id=player.id,
            username=player.username,
            total_wins=player.total_wins
        )
        for player in players
    ]
    
    return LeaderboardResponse(
        players=player_entries,
        ranking_type="wins"
    )

@router.get("/efficiency", response_model=LeaderboardResponse) 
def get_leaderboard_by_efficiency(db: Session = Depends(get_db)):
    """Get top 3 players by efficiency (moves per win)."""
    players_with_efficiency = leaderboard_service.get_top_players_by_efficiency(db, 3)
    
    player_entries = [
        LeaderboardPlayer(
            id=player['id'],
            username=player['username'],
            total_wins=player['total_wins'],
            efficiency=player['avg_moves_per_win']
        )
        for player in players_with_efficiency
    ]
    
    return LeaderboardResponse(
        players=player_entries,
        ranking_type="efficiency"
    )