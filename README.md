# Nclusion-grid-game
## How to run: 
``` bash
 uvicorn app.main:app --reload 
 ```
## Testing

To run the tests:

```bash
# Run all tests
pytest

# Run all tests with coverage
pytest --cov=app --cov-report=term-missing --cov-report=html --cov-config=.coveragerc

```

## ER Diagram
```mermaid

erDiagram
    PLAYER {
        int id PK
        string username UK "Display name for player"
        string email UK "Email"
        datetime created_at 
        int total_games "Tracking leaderboard performance"
        int total_wins "Tracking leaderboard ranking"
        float win_rate "Track player efficiency"
    }

    GAME_SESSION {
        int id PK 
        string session_code UK "UUID for players to join"
        enum status "WAITING/ACTIVE/COMPLETED"
        json game_state "3x3 array [[0,1,2],[0,0,0],[0,0,0]] - game board"
        int current_turn_player_id FK "Whose turn it is"
        int winner_id FK 
        enum game_result "WIN/DRAW"
        datetime created_at 
        datetime started_at 
        datetime ended_at 
        int player1_id FK 
        int player2_id FK 
    }

    MOVE {
        int id PK 
        int session_id FK 
        int player_id FK 
        int row_position 
        int col_position 
    }

    %% Primary Relationships
    PLAYER ||--o{ GAME_SESSION : "player1_creates"
    PLAYER ||--o{ GAME_SESSION : "player2_joins"
    PLAYER ||--o{ GAME_SESSION : "current_turn"
    PLAYER ||--o{ GAME_SESSION : "wins"
    
    GAME_SESSION ||--o{ MOVE : "contains"
    PLAYER ||--o{ MOVE : "makes"

```