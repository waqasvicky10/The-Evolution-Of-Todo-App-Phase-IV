
"""
Task service for CRUD operations with user isolation.

This module provides business logic for task management operations.
All operations enforce user data isolation - users can only access their own tasks.
"""
from typing import Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status
from datetime import datetime
from typing import List
from app.models.task import Task


def get_user_tasks(db: Session, user_id: int, completed: Optional[bool] = None, priority: Optional[str] = None, category: Optional[str] = None) -> List[Task]:
    """
    Get tasks for a specific user with optional filters.

    Args:
        db: Database session
        user_id: User ID to filter tasks
        completed: Filter by completion status
        priority: Filter by priority level
        category: Filter by category

    Returns:
        List of tasks belonging to the user matching filters
    """
    statement = select(Task).where(Task.user_id == user_id)
    
    if completed is not None:
        statement = statement.where(Task.is_complete == completed)
    if priority:
        statement = statement.where(Task.priority == priority)
    if category:
        statement = statement.where(Task.category == category)
        
    tasks = db.exec(statement).all()
    return list(tasks)


def create_task(db: Session, user_id: int, description: str) -> Task:
    """
    Create a new task for a user.

    Args:
        db: Database session
        user_id: User ID (task owner)
        description: Task description

    Returns:
        Created task object

    Example:
        >>> task = create_task(db, user_id=1, description="Buy groceries")
        >>> print(task.id)
        1
        >>> print(task.user_id)
        1
    """
    task = Task(description=description, user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(db: Session, task_id: int, user_id: int) -> Task:
    """
    Get a specific task by ID with user isolation check.

    CRITICAL: This function enforces user data isolation.
    Query filters by BOTH task_id AND user_id to ensure users can only
    access their own tasks.

    Args:
        db: Database session
        task_id: Task ID
        user_id: User ID (must be task owner)

    Returns:
        Task object if found and belongs to user

    Raises:
        HTTPException 404: If task not found OR belongs to different user
                           (same error for security - don't leak task existence)

    Example:
        >>> task = get_task_by_id(db, task_id=1, user_id=1)
        >>> print(task.description)
        Buy groceries

        >>> # User 2 trying to access User 1's task
        >>> task = get_task_by_id(db, task_id=1, user_id=2)
        HTTPException: 404 Task not found
    """
    task = db.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        # Return 404 whether task doesn't exist OR belongs to different user
        # Don't reveal if task exists (security best practice)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


def update_task(db: Session, task_id: int, user_id: int, description: str) -> Task:
    """
    Update a task's description with user isolation check.

    Args:
        db: Database session
        task_id: Task ID
        user_id: User ID (must be task owner)
        description: New task description

    Returns:
        Updated task object

    Raises:
        HTTPException 404: If task not found or belongs to different user

    Example:
        >>> task = update_task(db, task_id=1, user_id=1, description="Buy groceries and cook")
        >>> print(task.description)
        Buy groceries and cook
    """
    # get_task_by_id enforces user isolation
    task = get_task_by_id(db, task_id, user_id)

    # Update task
    task.description = description
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: int, user_id: int) -> None:
    """
    Delete a task with user isolation check.

    Args:
        db: Database session
        task_id: Task ID
        user_id: User ID (must be task owner)

    Returns:
        None

    Raises:
        HTTPException 404: If task not found or belongs to different user

    Example:
        >>> delete_task(db, task_id=1, user_id=1)
        # Task deleted successfully
    """
    # get_task_by_id enforces user isolation
    task = get_task_by_id(db, task_id, user_id)

    # Delete task
    db.delete(task)
    db.commit()


def toggle_task(db: Session, task_id: int, user_id: int) -> Task:
    """
    Toggle a task's completion status with user isolation check.

    Args:
        db: Database session
        task_id: Task ID
        user_id: User ID (must be task owner)

    Returns:
        Updated task object with toggled is_complete status

    Raises:
        HTTPException 404: If task not found or belongs to different user

    Example:
        >>> task = toggle_task(db, task_id=1, user_id=1)
        >>> print(task.is_complete)
        True
        >>> task = toggle_task(db, task_id=1, user_id=1)
        >>> print(task.is_complete)
        False
    """
    # get_task_by_id enforces user isolation
    task = get_task_by_id(db, task_id, user_id)

    # Toggle completion status
    task.is_complete = not task.is_complete
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)

    return task
