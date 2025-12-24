"""
This is the main file.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os
from app.api import endpoints
from app.db.database import engine, Base

# Create DB tables.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intelligent Query-Retrieval System API")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api/v1", tags=["query"])

# --- NEW SECTION TO SERVE REACT FRONTEND ---

# Define the path to the frontend build directory
build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "build"))

# Mount the static files (JS, CSS, etc.) from the React build folder
app.mount("/static", StaticFiles(directory=os.path.join(build_dir, "static")), name="static")

# A catch-all route to serve the index.html for any other path
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    return FileResponse(os.path.join(build_dir, "index.html"))