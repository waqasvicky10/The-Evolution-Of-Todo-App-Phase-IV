"""
Vercel serverless function entry point for FastAPI backend.
Exports the FastAPI app instance for Vercel's Python runtime.
"""
import os
os.environ.setdefault("ENVIRONMENT", "production")

from app.main import app
