from fastapi import FastAPI
from app.database import engine, Base
from app.player.routes import router as player_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Grid Game Engine")

app.include_router(player_router, prefix="/api/v1/players", tags=["players"])

@app.get("/")
def root():
    return {"message": "Grid Game Engine API"}