from app.core.engine import GameEngine
from app.game_session.service import GameSessionService

def test_check_winner_row():
    grid = [[1, 1, 1], [0, 0, 0], [0, 0, 0]]
    assert GameEngine.check_winner(grid, 1) == True
    assert GameEngine.check_winner(grid, 2) == False

def test_check_winner_column():
    grid = [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
    assert GameEngine.check_winner(grid, 1) == True

def test_check_winner_diagonal():
    grid = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert GameEngine.check_winner(grid, 1) == True

def test_check_winner_anti_diagonal():
    grid = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    assert GameEngine.check_winner(grid, 1) == True

def test_is_board_full():
    full_grid = [[1, 2, 1], [2, 1, 2], [1, 2, 1]]
    empty_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    partial_grid = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    assert GameEngine.is_board_full(full_grid) == True
    assert GameEngine.is_board_full(empty_grid) == False
    assert GameEngine.is_board_full(partial_grid) == False

def test_is_valid_move_with_api(client, db_session):
    
    player1_response = client.post("/api/v1/player/", json={
        "username": "player1",
        "email": "player1@test.com"
    })
    assert player1_response.status_code == 200
    player1 = player1_response.json()
    
    player2_response = client.post("/api/v1/player/", json={
        "username": "player2", 
        "email": "player2@test.com"
    })
    assert player2_response.status_code == 200
    player2 = player2_response.json()
    
    create_session_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    assert create_session_response.status_code == 200
    session_data = create_session_response.json()
    
    join_response = client.post(f"/api/v1/gameSession/join/{session_data['session_code']}", json={
        "player_id": player2["id"]
    })
    assert join_response.status_code == 200
    join_data = join_response.json()
    
    session_response = client.get(f"/api/v1/gameSession/{join_data['session_id']}")
    assert session_response.status_code == 200
    
    
    game_session_service = GameSessionService()
    session = game_session_service.get_game_session(db_session, join_data['session_id'])
    
    assert GameEngine.is_valid_move(session, player1["id"], 0, 0) == True
    
    # Test invalid moves
    assert GameEngine.is_valid_move(session, player2["id"], 0, 0) == False  
    assert GameEngine.is_valid_move(session, player1["id"], 3, 0) == False  
    assert GameEngine.is_valid_move(session, player1["id"], 0, -1) == False  
    
    # Occupies test
    session.game_state[0][0] = player1["id"]
    assert GameEngine.is_valid_move(session, player1["id"], 0, 0) == False
