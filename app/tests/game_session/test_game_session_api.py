import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def test_players(client):
    """Create two test players."""
    player1_response = client.post("/api/v1/player/", json={
        "username": "player1",
        "email": "player1@test.com"
    })
    player2_response = client.post("/api/v1/player/", json={
        "username": "player2", 
        "email": "player2@test.com"
    })
    return player1_response.json(), player2_response.json()

def test_create_session_success(client: TestClient, test_players):
    player1, player2 = test_players
    
    response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "session_code" in data
    assert data["status"] == "WAITING"

def test_create_session_invalid_player(client: TestClient):
    response = client.post("/api/v1/gameSession/create", json={
        "player_id": 999
    })
    
    assert response.status_code == 404
    assert "Player not found" in response.json()["detail"]

def test_join_session_success(client: TestClient, test_players):
    player1, player2 = test_players
    
    # Create session
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    session_code = create_response.json()["session_code"]
    
    # Join session
    response = client.post(f"/api/v1/gameSession/join/{session_code}", json={
        "player_id": player2["id"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["game_started"] == True
    assert data["status"] == "ACTIVE"
    assert data["player1_id"] == player1["id"]
    assert data["player2_id"] == player2["id"]

def test_join_session_not_found(client: TestClient, test_players):
    player1, player2 = test_players
    
    response = client.post("/api/v1/gameSession/join/INVALID", json={
        "player_id": player2["id"]
    })
    
    assert response.status_code == 400
    assert "Session not found" in response.json()["detail"]

def test_join_own_session(client: TestClient, test_players):
    player1, player2 = test_players
    
    # Create session
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    session_code = create_response.json()["session_code"]
    
    # Try to join own session
    response = client.post(f"/api/v1/gameSession/join/{session_code}", json={
        "player_id": player1["id"]
    })
    
    assert response.status_code == 400
    assert "Cannot join your own session" in response.json()["detail"]

def test_get_session_success(client: TestClient, test_players):
    player1, player2 = test_players
    
    # Create session
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player1["id"]
    })
    session_id = create_response.json()["session_id"]
    
    # Get session
    response = client.get(f"/api/v1/gameSession/{session_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == session_id
    assert data["status"] == "WAITING"
    assert data["game_state"] == [[0,0,0],[0,0,0],[0,0,0]]