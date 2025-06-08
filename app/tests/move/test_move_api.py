from fastapi.testclient import TestClient

def test_make_move_success(client: TestClient):
    player1_response = client.post("/api/v1/player/", json={
        "username": "player1",
        "email": "player1@test.com"
    })
    player1 = player1_response.json()
    
    player2_response = client.post("/api/v1/player/", json={
        "username": "player2",
        "email": "player2@test.com"
    })
    player2 = player2_response.json()
    
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    session_data = create_response.json()
    
    join_response = client.post(f"/api/v1/gameSession/join/{session_data['session_code']}", json={
        "player_id": player2["id"]
    })
    session_id = join_response.json()["session_id"]
    
    move_response = client.post("/api/v1/move/", json={
        "session_id": session_id,
        "player_id": player1["id"],
        "row": 0,
        "col": 0
    })
    
    assert move_response.status_code == 200
    move_data = move_response.json()
    assert "id" in move_data
    
    assert move_data["game_state"][0][0] == player1["id"]
    assert move_data["game_status"] == "ACTIVE"
    assert move_data["winner_id"] is None
    assert move_data["current_turn_player_id"] == player2["id"] 

def test_make_move_invalid_session(client: TestClient):
    response = client.post("/api/v1/move/", json={
        "session_id": 999,
        "player_id": 1,
        "row": 0,
        "col": 0
    })
    
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]

def test_make_move_wrong_turn(client: TestClient):
    player1_response = client.post("/api/v1/player/", json={
        "username": "player1",
        "email": "player1@test.com"
    })
    player1 = player1_response.json()
    
    player2_response = client.post("/api/v1/player/", json={
        "username": "player2",
        "email": "player2@test.com"
    })
    player2 = player2_response.json()
    
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    session_data = create_response.json()
    
    join_response = client.post(f"/api/v1/gameSession/join/{session_data['session_code']}", json={
        "player_id": player2["id"]
    })
    session_id = join_response.json()["session_id"]
    
    response = client.post("/api/v1/move/", json={
        "session_id": session_id,
        "player_id": player2["id"],
        "row": 0,
        "col": 0
    })
    
    assert response.status_code == 400
    assert "Not your turn" in response.json()["detail"]

def test_make_move_out_of_bounds(client: TestClient):
    response = client.post("/api/v1/move/", json={
        "session_id": 1,
        "player_id": 1,
        "row": 3,  
        "col": 0
    })
    
    assert response.status_code == 422  

def test_make_move_cell_occupied(client: TestClient):
    player1_response = client.post("/api/v1/player/", json={
        "username": "player1",
        "email": "player1@test.com"
    })
    player1 = player1_response.json()
    
    player2_response = client.post("/api/v1/player/", json={
        "username": "player2",
        "email": "player2@test.com"
    })
    player2 = player2_response.json()
    
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    session_data = create_response.json()
    
    join_response = client.post(f"/api/v1/gameSession/join/{session_data['session_code']}", json={
        "player_id": player2["id"]
    })
    session_id = join_response.json()["session_id"]
    
    client.post("/api/v1/move/", json={
        "session_id": session_id,
        "player_id": player1["id"],
        "row": 0,
        "col": 0
    })
    
    response = client.post("/api/v1/move/", json={
        "session_id": session_id,
        "player_id": player2["id"],
        "row": 0,
        "col": 0  
    })
    
    assert response.status_code == 400
    assert "Cell already occupied" in response.json()["detail"]

def test_get_session_moves_success(client: TestClient):
    player1_response = client.post("/api/v1/player/", json={
        "username": "player1",
        "email": "player1@test.com"
    })
    player1 = player1_response.json()
    
    player2_response = client.post("/api/v1/player/", json={
        "username": "player2",
        "email": "player2@test.com"
    })
    player2 = player2_response.json()
    
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    session_data = create_response.json()
    
    join_response = client.post(f"/api/v1/gameSession/join/{session_data['session_code']}", json={
        "player_id": player2["id"]
    })
    session_id = join_response.json()["session_id"]
    
    client.post("/api/v1/move/", json={
        "session_id": session_id,
        "player_id": player1["id"],
        "row": 0,
        "col": 0
    })
    
    client.post("/api/v1/move/", json={
        "session_id": session_id,
        "player_id": player2["id"],
        "row": 1,
        "col": 1
    })
    
    response = client.get(f"/api/v1/move/session/{session_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["session_id"] == session_id
    assert data["total_moves"] == 2
    assert len(data["moves"]) == 2
    
    first_move = data["moves"][0]
    assert first_move["session_id"] == session_id
    assert first_move["player_id"] == player1["id"]
    assert first_move["row_position"] == 0
    assert first_move["col_position"] == 0

def test_get_session_moves_invalid_session(client: TestClient):
    response = client.get("/api/v1/move/session/999")
    
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]

def test_get_session_moves_empty(client: TestClient):
    player1_response = client.post("/api/v1/player/", json={
        "username": "player1",
        "email": "player1@test.com"
    })
    player1 = player1_response.json()
    
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    session_data = create_response.json()
    
    response = client.get(f"/api/v1/move/session/{session_data['session_id']}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["session_id"] == session_data["session_id"]
    assert data["total_moves"] == 0
    assert len(data["moves"]) == 0

def test_get_specific_move_success(client: TestClient):
    player1_response = client.post("/api/v1/player/", json={
        "username": "player1",
        "email": "player1@test.com"
    })
    player1 = player1_response.json()
    
    player2_response = client.post("/api/v1/player/", json={
        "username": "player2",
        "email": "player2@test.com"
    })
    player2 = player2_response.json()
    
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    session_data = create_response.json()
    
    join_response = client.post(f"/api/v1/gameSession/join/{session_data['session_code']}", json={
        "player_id": player2["id"]
    })
    session_id = join_response.json()["session_id"]
    
    move_response = client.post("/api/v1/move/", json={
        "session_id": session_id,
        "player_id": player1["id"],
        "row": 1,
        "col": 2
    })
    move_id = move_response.json()["id"]
    
    response = client.get(f"/api/v1/move/{move_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == move_id
    assert data["session_id"] == session_id
    assert data["player_id"] == player1["id"]
    assert data["row_position"] == 1
    assert data["col_position"] == 2

def test_get_specific_move_not_found(client: TestClient):
    response = client.get("/api/v1/move/999")
    
    assert response.status_code == 404
    assert "Move not found" in response.json()["detail"]

def test_invalid_position_validation(client: TestClient):
    response = client.post("/api/v1/move/", json={
        "session_id": 1,
        "player_id": 1,
        "row": -1,
        "col": 0
    })
    assert response.status_code == 422
    
    response = client.post("/api/v1/move/", json={
        "session_id": 1,
        "player_id": 1,
        "row": 3,
        "col": 0
    })
    assert response.status_code == 422

def test_missing_fields_validation(client: TestClient):
    response = client.post("/api/v1/move/", json={
        "player_id": 1,
        "row": 0,
        "col": 0
    })
    assert response.status_code == 422

def test_winning_game_moves(client: TestClient):
    player1_response = client.post("/api/v1/player/", json={
        "username": "winner",
        "email": "winner@test.com"
    })
    player1 = player1_response.json()
    
    player2_response = client.post("/api/v1/player/", json={
        "username": "loser",
        "email": "loser@test.com"
    })
    player2 = player2_response.json()
    
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    session_data = create_response.json()
    
    join_response = client.post(f"/api/v1/gameSession/join/{session_data['session_code']}", json={
        "player_id": player2["id"]
    })
    session_id = join_response.json()["session_id"]
    
    moves = [
        {"player_id": player1["id"], "row": 0, "col": 0},  
        {"player_id": player2["id"], "row": 1, "col": 0},  
        {"player_id": player1["id"], "row": 0, "col": 1},  
        {"player_id": player2["id"], "row": 1, "col": 1},  
        {"player_id": player1["id"], "row": 0, "col": 2},  # Player 1 WINS!
    ]
    
    for i, move in enumerate(moves):
        response = client.post("/api/v1/move/", json={
            "session_id": session_id,
            "player_id": move["player_id"],
            "row": move["row"],
            "col": move["col"]
        })
        
        assert response.status_code == 200
        move_data = response.json()
        
        if i == len(moves) - 1: 
            assert move_data["winner_id"] == player1["id"]
            assert move_data["game_status"] == "COMPLETED"
        else:
            assert move_data["winner_id"] is None
            assert move_data["game_status"] == "ACTIVE"