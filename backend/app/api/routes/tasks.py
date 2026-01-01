"""
Task management API routes.

This module provides endpoints for task CRUD operations.
All endpoints require authentication and enforce user data isolation.
"""

from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.schemas.task import TaskCreate, TaskUpdate, TaskListResponse, TaskResponse
from app.services.task_service import create_task, get_task_by_id, get_user_tasks, update_task, delete_task, toggle_task
from app.api.deps import get_db, get_current_user
from app.models.user import User


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all tasks for the authenticated user.

    Returns only tasks that belong to the authenticated user (user isolation).

    Args:
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        List of tasks and total count

    Requires:
        Valid JWT token in Authorization header

    Raises:
        401: Not authenticated or invalid token

    Example:
        GET /api/tasks
        Headers: Authorization: Bearer <access_token>

        Response 200:
        {
            "tasks": [
                {
                    "id": 1,
                    "description": "Buy groceries",
                    "is_complete": false,
                    "user_id": 1,
                    "created_at": "2026-01-01T12:00:00Z",
                    "updated_at": "2026-01-01T12:00:00Z"
                }
            ],
            "total": 1
        }
    """
    tasks = get_user_tasks(db, user_id=current_user.id)
    return TaskListResponse(
        tasks=[TaskResponse.model_validate(task) for task in tasks],
        total=len(tasks)
    )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    request: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user.

    Creates a task with the provided description. The task is automatically
    associated with the authenticated user and starts in incomplete state.

    Args:
        request: Task creation request with description
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        Created task object with timestamps

    Requires:
        Valid JWT token in Authorization header

    Raises:
        401: Not authenticated or invalid token
        422: Validation error (empty description, too long, etc.)

    Example:
        POST /api/tasks
        Headers: Authorization: Bearer <access_token>
        {
            "description": "Buy groceries"
        }

        Response 201:
        {
            "id": 1,
            "description": "Buy groceries",
            "is_complete": false,
            "user_id": 1,
            "created_at": "2026-01-01T12:00:00Z",
            "updated_at": "2026-01-01T12:00:00Z"
        }
    """
    task = create_task(db, user_id=current_user.id, description=request.description)
    return TaskResponse.model_validate(task)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID.

    Returns a single task if it exists and belongs to the authenticated user.
    Enforces user data isolation - users cannot access other users' tasks.

    Args:
        task_id: Task ID from URL path
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        Task object with all details

    Requires:
        Valid JWT token in Authorization header

    Raises:
        401: Not authenticated or invalid token
        404: Task not found OR task belongs to different user
             (same error for security - don't leak task existence)

    Example:
        GET /api/tasks/1
        Headers: Authorization: Bearer <access_token>

        Response 200:
        {
            "id": 1,
            "description": "Buy groceries",
            "is_complete": false,
            "user_id": 1,
            "created_at": "2026-01-01T12:00:00Z",
            "updated_at": "2026-01-01T12:00:00Z"
        }
    """
    task = get_task_by_id(db, task_id=task_id, user_id=current_user.id)
    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    request: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a task's description.

    Updates the description of an existing task. Only the task owner can
    update it. The updated_at timestamp is automatically updated.

    Args:
        task_id: Task ID from URL path
        request: Task update request with new description
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        Updated task object

    Requires:
        Valid JWT token in Authorization header

    Raises:
        401: Not authenticated or invalid token
        404: Task not found OR task belongs to different user
        422: Validation error (empty description, too long, etc.)

    Example:
        PUT /api/tasks/1
        Headers: Authorization: Bearer <access_token>
        {
            "description": "Buy groceries and cook dinner"
        }

        Response 200:
        {
            "id": 1,
            "description": "Buy groceries and cook dinner",
            "is_complete": false,
            "user_id": 1,
            "created_at": "2026-01-01T12:00:00Z",
            "updated_at": "2026-01-01T13:00:00Z"
        }
    """
    task = update_task(db, task_id=task_id, user_id=current_user.id, description=request.description)
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task.

    Permanently deletes a task. Only the task owner can delete it.
    This operation cannot be undone.

    Args:
        task_id: Task ID from URL path
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        No content (204 status code)

    Requires:
        Valid JWT token in Authorization header

    Raises:
        401: Not authenticated or invalid token
        404: Task not found OR task belongs to different user

    Example:
        DELETE /api/tasks/1
        Headers: Authorization: Bearer <access_token>

        Response 204: (No content)
    """
    delete_task(db, task_id=task_id, user_id=current_user.id)


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
def toggle_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle a task's completion status.

    Toggles the is_complete status of a task between true and false.
    If the task is incomplete, it becomes complete. If complete, it becomes incomplete.
    Only the task owner can toggle it. The updated_at timestamp is automatically updated.

    Args:
        task_id: Task ID from URL path
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        Updated task object with toggled is_complete status

    Requires:
        Valid JWT token in Authorization header

    Raises:
        401: Not authenticated or invalid token
        404: Task not found OR task belongs to different user

    Example:
        PATCH /api/tasks/1/toggle
        Headers: Authorization: Bearer <access_token>

        Response 200 (if task was incomplete):
        {
            "id": 1,
            "description": "Buy groceries",
            "is_complete": true,
            "user_id": 1,
            "created_at": "2026-01-01T12:00:00Z",
            "updated_at": "2026-01-01T14:00:00Z"
        }

        Response 200 (if task was complete):
        {
            "id": 1,
            "description": "Buy groceries",
            "is_complete": false,
            "user_id": 1,
            "created_at": "2026-01-01T12:00:00Z",
            "updated_at": "2026-01-01T15:00:00Z"
        }
    """
    task = toggle_task(db, task_id=task_id, user_id=current_user.id)
    return TaskResponse.model_validate(task)
