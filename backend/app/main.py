"""
FastAPI application entry point.

Main application instance with CORS configuration and route registration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import auth, tasks, chat
from app.routes import ai
from app.database import init_db
# Create FastAPI application
app = FastAPI(
    title="Todo API - Phase II",
    description="Multi-user todo application with authentication",
    version="2.0.0"
)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    """Fast startup - database tables created via init_db or migrations."""
    print("[Startup] Server starting (database tables initialization)")
    init_db()


# Configure CORS - allow specific origins for development
# Wildcard ["*"] is not allowed when allow_credentials=True
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(ai.router)
app.include_router(chat.router)  # Phase III chat endpoints


@app.get("/")
def root():
    """
    Root endpoint.

    Returns:
        API information and status
    """
    return {
        "message": "Todo API Phase II",
        "version": "2.0.0",
        "status": "running"
    }
