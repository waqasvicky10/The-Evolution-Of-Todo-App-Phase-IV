"""
AI-powered task management endpoints.

Provides intelligent task analysis, suggestions, and improvements
using OpenAI integration.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from ..database import get_session
from ..models.user import User
from ..api.deps import get_current_user
from ..services.ai_service import ai_service, TaskSuggestion, TaskAnalysis


router = APIRouter(prefix="/api/ai", tags=["AI Features"])


# ============================================================================
# Request/Response Models
# ============================================================================

class TaskAnalysisRequest(BaseModel):
    """Request model for task analysis."""
    description: str
    user_context: Dict[str, Any] = {}


class TaskSuggestionRequest(BaseModel):
    """Request model for task suggestions."""
    count: int = 5
    user_context: Dict[str, Any] = {}


class TaskImprovementRequest(BaseModel):
    """Request model for task description improvement."""
    description: str


class AIStatusResponse(BaseModel):
    """Response model for AI service status."""
    available: bool
    message: str


# ============================================================================
# AI Status Endpoint
# ============================================================================

@router.get("/status", response_model=AIStatusResponse)
async def get_ai_status():
    """
    Get AI service availability status.
    
    Returns:
        AI service status and availability message
    """
    is_available = ai_service.is_available()
    message = "AI features are available" if is_available else "AI features are disabled - OpenAI API key not configured"
    
    return AIStatusResponse(
        available=is_available,
        message=message
    )


# ============================================================================
# Task Analysis Endpoint
# ============================================================================

@router.post("/analyze-task", response_model=TaskAnalysis)
async def analyze_task(
    request: TaskAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Analyze a task description using AI.
    
    Args:
        request: Task analysis request with description and context
        current_user: Authenticated user
        db: Database session
        
    Returns:
        AI analysis with category, priority, tags, and suggestions
    """
    try:
        # Add user ID to context
        user_context = request.user_context.copy()
        user_context["user_id"] = current_user.id
        
        analysis = await ai_service.analyze_task(
            description=request.description,
            user_context=user_context
        )
        
        return analysis
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Task analysis failed: {str(e)}"
        )


# ============================================================================
# Task Suggestions Endpoint
# ============================================================================

@router.post("/suggest-tasks", response_model=List[TaskSuggestion])
async def suggest_tasks(
    request: TaskSuggestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get AI-powered task suggestions.
    
    Args:
        request: Task suggestion request with count and context
        current_user: Authenticated user
        db: Database session
        
    Returns:
        List of AI-generated task suggestions
    """
    try:
        # Add user ID and basic user info to context
        user_context = request.user_context.copy()
        user_context.update({
            "user_id": current_user.id,
            "user_email": current_user.email,
            "request_count": request.count
        })
        
        suggestions = await ai_service.suggest_tasks(
            user_context=user_context,
            count=min(request.count, 10)  # Limit to 10 suggestions max
        )
        
        return suggestions
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Task suggestions failed: {str(e)}"
        )


# ============================================================================
# Task Improvement Endpoint
# ============================================================================

@router.post("/improve-task", response_model=Dict[str, str])
async def improve_task_description(
    request: TaskImprovementRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Improve a task description using AI.
    
    Args:
        request: Task improvement request with original description
        current_user: Authenticated user
        
    Returns:
        Original and improved task descriptions
    """
    try:
        improved_description = await ai_service.improve_task_description(
            description=request.description
        )
        
        return {
            "original": request.description,
            "improved": improved_description
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Task improvement failed: {str(e)}"
        )


# ============================================================================
# Smart Task Creation Endpoint
# ============================================================================

@router.post("/smart-create", response_model=Dict[str, Any])
async def smart_task_creation(
    request: TaskAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Create a task with AI analysis and improvements.
    
    Args:
        request: Task creation request with description and context
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Enhanced task data with AI analysis and improved description
    """
    try:
        # Get AI analysis
        user_context = request.user_context.copy()
        user_context["user_id"] = current_user.id
        
        analysis = await ai_service.analyze_task(
            description=request.description,
            user_context=user_context
        )
        
        # Improve description
        improved_description = await ai_service.improve_task_description(
            description=request.description
        )
        
        return {
            "original_description": request.description,
            "improved_description": improved_description,
            "analysis": analysis.dict(),
            "ready_to_create": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Smart task creation failed: {str(e)}"
        )