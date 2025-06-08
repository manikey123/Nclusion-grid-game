from fastapi import FastAPI
from app.database import engine, Base
from app.player.routes import router as player_router
from app.game_session.routes import router as game_session_router
from app.move.routes import router as move_router
from app.leaderboard.routes import router as leaderboard_router
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Grid Game Engine")

app.include_router(player_router, prefix="/api/v1/player", tags=["player"])
app.include_router(game_session_router, prefix="/api/v1/gameSession", tags=["gameSession"])
app.include_router(move_router, prefix="/api/v1/move", tags=["move"])
app.include_router(leaderboard_router, prefix="/api/v1/leaderboard", tags=["leaderboard"])

@app.get("/")
def root():
    return {"message": "Grid Game Engine API"}