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


# Skip database initialization on startup for faster server start
# Tables will be created by Alembic migrations or on first use
@app.on_event("startup")
async def startup_event():
    """Fast startup - database tables created via migrations."""
    print("[Startup] Server starting (database tables should be created via migrations)")
    # Don't call init_db() - it's slow and tables should exist from migrations
    # If tables don't exist, they'll be created on first request (slower but server starts fast)


# Configure CORS - allow all localhost origins for development
# Using allow_origins=["*"] for development to fix CORS issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development (change in production)
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


@app.get("/health")
def health_check():
    """
    Health check endpoint.

    Returns:
        Health status
    """
    return {"status": "healthy"}
