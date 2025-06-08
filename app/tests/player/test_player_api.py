from fastapi.testclient import TestClient

def test_create_player_success(client: TestClient):
    response = client.post("/api/v1/players/", json={
        "username": "testuser",
        "email": "test@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["total_games"] == 0
    assert data["total_wins"] == 0
    assert data["win_rate"] == 0.0

def test_create_player_duplicate_username(client: TestClient):
    # Create first player
    client.post("/api/v1/players/", json={
        "username": "testuser",
        "email": "test1@example.com"
    })
    
    # Try to create player with same username
    response = client.post("/api/v1/players/", json={
        "username": "testuser",
        "email": "test2@example.com"
    })
    assert response.status_code == 400
    assert "Username already exists" in response.json()["detail"]

def test_create_player_duplicate_email(client: TestClient):
    # Create first player
    client.post("/api/v1/players/", json={
        "username": "testuser1",
        "email": "test@example.com"
    })
    
    # Try to create player with same email
    response = client.post("/api/v1/players/", json={
        "username": "testuser2",
        "email": "test@example.com"
    })
    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]

def test_get_player_success(client: TestClient):
    create_response = client.post("/api/v1/players/", json={
        "username": "testuser",
        "email": "test@example.com"
    })
    player_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/players/{player_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == player_id
    assert data["username"] == "testuser"

def test_get_player_not_found(client: TestClient):
    response = client.get("/api/v1/players/999")
    assert response.status_code == 404
    assert "Player not found" in response.json()["detail"]