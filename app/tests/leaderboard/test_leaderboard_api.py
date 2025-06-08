from fastapi.testclient import TestClient
from app.leaderboard.service import LeaderboardService

def test_get_leaderboard_by_wins_empty(client: TestClient):
    response = client.get("/api/v1/leaderboard/wins")
    
    assert response.status_code == 200
    data = response.json()
    assert data["ranking_type"] == "wins"
    assert data["players"] == []

def test_get_leaderboard_by_efficiency_empty(client: TestClient):
    response = client.get("/api/v1/leaderboard/efficiency")
    
    assert response.status_code == 200
    data = response.json()
    assert data["ranking_type"] == "efficiency"
    assert data["players"] == []

def test_get_leaderboard_by_wins_with_players(client: TestClient):
    client.post("/api/v1/player/", json={
        "username": "player1", "email": "player1@test.com"
    }).json()
    
    client.post("/api/v1/player/", json={
        "username": "player2", "email": "player2@test.com"
    }).json()
    
    response = client.get("/api/v1/leaderboard/wins")
    
    assert response.status_code == 200
    data = response.json()
    assert data["ranking_type"] == "wins"
    assert len(data["players"]) == 2
    
    for player in data["players"]:
        assert player["total_wins"] == 0

def test_leaderboard_by_wins_with_completed_games(client: TestClient, db_session):
    player1 = client.post("/api/v1/player/", json={
        "username": "winner", "email": "winner@test.com"
    }).json()
    
    player2 = client.post("/api/v1/player/", json={
        "username": "loser", "email": "loser@test.com"
    }).json()
    
    player3 = client.post("/api/v1/player/", json={
        "username": "champion", "email": "champion@test.com"
    }).json()
    
    # Simulate games where player3 wins 2, player1 wins 1, player2 wins 0
    
    # Game 1: player3 vs player1 (player3 wins)
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": player3["id"]
    })
    session_code = create_response.json()["session_code"]
    
    join_response = client.post(f"/api/v1/gameSession/join/{session_code}", json={
        "player_id": player1["id"]
    })
    session_id = join_response.json()["session_id"]
    
    # Play moves for player3 to win (top row)
    moves = [
        {"player_id": player3["id"], "row": 0, "col": 0},  
        {"player_id": player1["id"], "row": 1, "col": 0},  
        {"player_id": player3["id"], "row": 0, "col": 1},  
        {"player_id": player1["id"], "row": 1, "col": 1},  
        {"player_id": player3["id"], "row": 0, "col": 2},  # player3 wins!
    ]
    
    for move in moves:
        client.post("/api/v1/move/", json={
            "session_id": session_id,
            "player_id": move["player_id"],
            "row": move["row"],
            "col": move["col"]
        })
    
    # Update player stats manually (since we don't have auto-update)
    leaderboard_service = LeaderboardService()
    leaderboard_service.update_player_stats(db_session, player3["id"])
    leaderboard_service.update_player_stats(db_session, player1["id"])
    leaderboard_service.update_player_stats(db_session, player2["id"])

    
    response = client.get("/api/v1/leaderboard/wins")
    
    assert response.status_code == 200
    data = response.json()
    assert data["ranking_type"] == "wins"
    assert len(data["players"]) <= 3 
    
    if data["players"]:
        top_player = data["players"][0]
        assert top_player["username"] == "champion"
        assert top_player["total_wins"] >= 1

def test_leaderboard_by_efficiency_with_games(client: TestClient, db_session):
    efficient_player = client.post("/api/v1/player/", json={
        "username": "efficient", "email": "efficient@test.com"
    }).json()
    
    inefficient_player = client.post("/api/v1/player/", json={
        "username": "inefficient", "email": "inefficient@test.com"
    }).json()
    
    # Create a quick game (efficient player wins in 5 moves)
    create_response = client.post("/api/v1/gameSession/create", json={
        "player_id": efficient_player["id"]
    })
    session_code = create_response.json()["session_code"]
    
    join_response = client.post(f"/api/v1/gameSession/join/{session_code}", json={
        "player_id": inefficient_player["id"]
    })
    session_id = join_response.json()["session_id"]
    
    # Efficient win (5 moves total)
    quick_win_moves = [
        {"player_id": efficient_player["id"], "row": 0, "col": 0},  
        {"player_id": inefficient_player["id"], "row": 1, "col": 0},  
        {"player_id": efficient_player["id"], "row": 0, "col": 1},  
        {"player_id": inefficient_player["id"], "row": 1, "col": 1},  
        {"player_id": efficient_player["id"], "row": 0, "col": 2}, 
    ]
    
    for move in quick_win_moves:
        client.post("/api/v1/move/", json={
            "session_id": session_id,
            "player_id": move["player_id"],
            "row": move["row"],
            "col": move["col"]
        })
    
    
    leaderboard_service = LeaderboardService()

    leaderboard_service.update_player_stats(db_session, efficient_player["id"])
    leaderboard_service.update_player_stats(db_session, inefficient_player["id"])
    
    response = client.get("/api/v1/leaderboard/efficiency")
    
    assert response.status_code == 200
    data = response.json()
    assert data["ranking_type"] == "efficiency"
    
    for player in data["players"]:
        if player["total_wins"] > 0:
            assert player["efficiency"] is not None
            assert player["efficiency"] > 0

def test_leaderboard_response_structure(client: TestClient):
    client.post("/api/v1/player/", json={
        "username": "testplayer", "email": "test@test.com"
    })
    
    response = client.get("/api/v1/leaderboard/wins")
    assert response.status_code == 200
    data = response.json()
    
    assert "players" in data
    assert "ranking_type" in data
    assert data["ranking_type"] == "wins"
    assert isinstance(data["players"], list)
    
    if data["players"]:
        player = data["players"][0]
        assert "id" in player
        assert "username" in player
        assert "total_wins" in player
        assert player.get("efficiency") is None
    
    response = client.get("/api/v1/leaderboard/efficiency")
    assert response.status_code == 200
    data = response.json()
    
    assert "players" in data
    assert "ranking_type" in data
    assert data["ranking_type"] == "efficiency"

def test_leaderboard_limits_to_top_3(client: TestClient):
    """Test that leaderboard returns max 3 players."""
    players = []
    for i in range(5):
        player = client.post("/api/v1/player/", json={
            "username": f"player{i}", 
            "email": f"player{i}@test.com"
        }).json()
        players.append(player)
    
    response = client.get("/api/v1/leaderboard/wins")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["players"]) <= 3

def test_leaderboard_ordering(client: TestClient):  
    response = client.get("/api/v1/leaderboard/wins")
    assert response.status_code == 200
    data = response.json()
    
    # Check that wins are in descending order
    previous_wins = float('inf')
    for player in data["players"]:
        current_wins = player["total_wins"]
        assert current_wins <= previous_wins
        previous_wins = current_wins