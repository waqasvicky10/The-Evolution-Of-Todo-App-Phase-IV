"""
Minimal FastAPI app for Vercel deployment
"""
from fastapi import FastAPI

app = FastAPI(title="Phase III Todo Chat API")


@app.get("/")
async def root():
    """Root endpoint to test deployment"""
    return {"status": "alive"}


@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {"status": "alive", "message": "Phase III Todo Chat API"}
