from typing import List
from app.game_session.models import GameSession, GameResult, GameSessionStatus
from datetime import datetime, timezone

class GameEngine:
    @staticmethod
    def is_valid_move(session: GameSession, player_id: int, row: int, col: int) -> bool:
        if session.status != GameSessionStatus.ACTIVE:
            return False
            
        if session.current_turn_player_id != player_id:
            return False
        
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return False
        
        if session.game_state[row][col] != 0:
            return False
            
        return True
    
    @staticmethod
    def make_move(session: GameSession, player_id: int, row: int, col: int) -> bool:
        if not GameEngine.is_valid_move(session, player_id, row, col):
            return False
        
        # We need to Deep copy because of complex Json column
        new_game_state = [row[:] for row in session.game_state]  
        new_game_state[row][col] = player_id
        session.game_state = new_game_state 
        
        if GameEngine.check_winner(session.game_state, player_id):
            session.winner_id = player_id
            session.game_result = GameResult.WIN
            session.status = GameSessionStatus.COMPLETED
            session.ended_at = datetime.now(timezone.utc)
            return True
        
        if GameEngine.is_board_full(session.game_state):
            session.game_result = GameResult.DRAW
            session.status = GameSessionStatus.COMPLETED
            session.ended_at = datetime.now(timezone.utc)
            return True
        
        session.current_turn_player_id = (
            session.player2_id if player_id == session.player1_id 
            else session.player1_id
        )
        
        return True
    
    @staticmethod
    def check_winner(grid: List[List[int]], player_id: int) -> bool:
        for row in grid:
            if all(cell == player_id for cell in row):
                return True
        
        for col in range(3):
            if all(grid[row][col] == player_id for row in range(3)):
                return True
        
        # Check diagonals
        if all(grid[i][i] == player_id for i in range(3)):
            return True
        if all(grid[i][2-i] == player_id for i in range(3)):
            return True
            
        return False
    
    @staticmethod
    def is_board_full(grid: List[List[int]]) -> bool:
        return all(cell != 0 for row in grid for cell in row)