"""
FastAPI Chat API Main Application for Vercel
"""
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Phase III Todo Chat API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_UI_DIR = os.path.join(BASE_DIR, "chat_ui")

# Try to import and include chat routes
try:
    from phase_iii.chat_api.routes.chat import router as chat_router
    from phase_iii.persistence.repositories.conversation_repo import init_conversation_tables
    from phase_iii.persistence.repositories.tool_call_repo import init_tool_call_tables
    from phase_iii.mcp_server.tools.todo_tools import init_todo_tables
    
    # Initialize database tables
    try:
        init_conversation_tables()
        init_tool_call_tables()
        init_todo_tables()
        logger.info("Database tables initialized")
    except Exception as e:
        logger.warning(f"Database initialization warning: {e}")
    
    # Include chat router (router already has prefix="/api" in its definition)
    app.include_router(chat_router)
    logger.info("Chat API routes included")
except Exception as e:
    logger.error(f"Failed to import chat routes: {e}", exc_info=True)
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    # Create a simple router for testing
    @app.get("/api/health")
    async def health():
        return {"status": "alive", "message": "Chat routes not available", "error": str(e)}
    
    @app.post("/api/chat")
    async def chat_fallback():
        return {"error": "Chat routes not available", "details": str(e)}
    
    @app.get("/api/chat/history")
    async def history_fallback():
        return {"error": "Chat routes not available", "details": str(e)}


# Serve static files from chat_ui directory
if os.path.exists(CHAT_UI_DIR):
    app.mount("/static", StaticFiles(directory=CHAT_UI_DIR), name="static")
    logger.info(f"Static files mounted from {CHAT_UI_DIR}")


# Root endpoint - serve the chat UI
@app.get("/")
async def root():
    """Serve the chat UI"""
    index_path = os.path.join(CHAT_UI_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "alive", "message": "Chat UI not found"}


# Serve other UI files
@app.get("/styles.css")
async def styles():
    """Serve CSS file"""
    css_path = os.path.join(CHAT_UI_DIR, "styles.css")
    if os.path.exists(css_path):
        return FileResponse(css_path, media_type="text/css")
    return {"error": "CSS not found"}


@app.get("/chat.js")
async def chat_js():
    """Serve JavaScript file"""
    js_path = os.path.join(CHAT_UI_DIR, "chat.js")
    if os.path.exists(js_path):
        return FileResponse(js_path, media_type="application/javascript")
    return {"error": "JavaScript not found"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "alive"}
