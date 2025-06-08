from sqlalchemy.orm import Session
from sqlalchemy import func
from app.player.models import Player
from app.game_session.models import GameSession
from typing import List

class LeaderboardService:
    
    def get_top_players_by_wins(self, db: Session, limit: int = 3) -> List[Player]:
        return db.query(Player).order_by(Player.total_wins.desc()).limit(limit).all()
    
    def get_top_players_by_efficiency(self, db: Session, limit: int = 3):
        players_with_wins = db.query(Player).filter(Player.total_wins > 0).all()
        
        efficiency_data = []
        
        for player in players_with_wins:
            # Get all games won by this player
            won_games = db.query(GameSession).filter(
                GameSession.winner_id == player.id
            ).all()
            
            if won_games:
                # Calculate average moves per win
                total_moves = 0
                for game in won_games:
                    moves_in_game = self.calculate_moves_from_game_state(game.game_state)
                    total_moves += moves_in_game
                
                avg_moves = total_moves / len(won_games)
                
                efficiency_data.append({
                    'id': player.id,
                    'username': player.username,
                    'total_wins': player.total_wins,
                    'avg_moves_per_win': avg_moves
                })
        
        # Sort by efficiency (lower average moves = better efficiency)
        efficiency_data.sort(key=lambda x: x['avg_moves_per_win'])
        
        return efficiency_data[:limit]
    
    def calculate_moves_from_game_state(self, game_state: List[List[int]]) -> int:
        return sum(1 for row in game_state for cell in row if cell != 0)
        
    def update_player_stats(self, db: Session, player_id: int):
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            return
        
        total_games = db.query(GameSession).filter(
            (GameSession.player1_id == player_id) | (GameSession.player2_id == player_id),
            GameSession.status == "COMPLETED"
        ).count()
        
        total_wins = db.query(GameSession).filter(
            GameSession.winner_id == player_id
        ).count()
        
        player.total_games = total_games
        player.total_wins = total_wins
        player.win_rate = total_wins / total_games if total_games > 0 else 0.0
        
        db.commit()