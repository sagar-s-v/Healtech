from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints
from app.db.database import engine, Base

# This line creates the database tables based on your models.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intelligent Query-Retrieval System API")

# This is the crucial CORS configuration block.
# It lists the frontend origins that are allowed to make requests to this backend.
origins = ["http://localhost:3000",
           "https://healtech-app.onrender.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allow specific origins
    allow_credentials=True,      # Allow cookies (if needed in the future)
    allow_methods=["*"],         # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],         # Allow all headers
)

# This line includes all the API routes from endpoints.py
app.include_router(endpoints.router, prefix="/api/v1", tags=["query"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Intelligent Query-Retrieval System API"}