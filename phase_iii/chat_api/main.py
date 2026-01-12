"""
FastAPI Chat API Main Application

This module creates and configures the FastAPI application for Phase III
chat functionality.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
# Add the parent directory to sys.path so 'phase_iii' can be found
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, parent_dir)
# Add the backend directory to sys.path so 'app' can be found
backend_path = os.path.join(parent_dir, "backend")
sys.path.append(backend_path)

from phase_iii.chat_api.routes.chat import router as chat_router
from phase_iii.persistence.repositories.conversation_repo import init_conversation_tables
from phase_iii.persistence.repositories.tool_call_repo import init_tool_call_tables
from phase_iii.mcp_server.tools.todo_tools import init_todo_tables

# Import Phase II routers and DB init
# Disabled for standalone Phase III demo
PHASE2_AVAILABLE = False
# try:
#     from app.api.routes import auth, tasks
#     from app.database import init_db as init_db_phase2
#     PHASE2_AVAILABLE = True
# except ImportError as e:
#     print(f"Warning: Phase II backend not found or incompatible: {e}")
#     PHASE2_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Todo Chat API",
    description="Phase III AI-Powered Todo Chatbot API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)

if PHASE2_AVAILABLE:
    app.include_router(auth.router)
    app.include_router(tasks.router)
    logger.info("Phase II routers (auth, tasks) integrated")


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    logger.info("Starting Chat API...")
    try:
        init_conversation_tables()
        init_tool_call_tables()
        init_todo_tables()
        if PHASE2_AVAILABLE:
            init_db_phase2()
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing tables: {e}", exc_info=True)
    logger.info("Chat API started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Chat API...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Todo Chat API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "chat_api"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
