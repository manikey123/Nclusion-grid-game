from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.database import engine, Base
from fastapi.responses import HTMLResponse


# Create the database tables
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Game Engine API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers

@app.get("/")
async def root():
    return HTMLResponse(content="<h1>Hello World</h1>", status_code=200)