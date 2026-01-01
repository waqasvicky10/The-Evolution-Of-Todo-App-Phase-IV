"""
Task request and response schemas.

Pydantic models for task CRUD operations with validation.
"""

from pydantic import BaseModel, constr, field_validator
from typing import List


class TaskCreate(BaseModel):
    """
    Task creation request schema.

    Validates description length and ensures it's not empty.
    """

    description: constr(min_length=1, max_length=500)

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """
        Validate description is not empty after stripping whitespace.

        Args:
            v: Description to validate

        Returns:
            Trimmed description if valid

        Raises:
            ValueError: If description is empty after stripping
        """
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Task description cannot be empty")
        return trimmed


class TaskUpdate(BaseModel):
    """
    Task update request schema.

    Validates new description length and ensures it's not empty.
    """

    description: constr(min_length=1, max_length=500)

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """
        Validate description is not empty after stripping whitespace.

        Args:
            v: Description to validate

        Returns:
            Trimmed description if valid

        Raises:
            ValueError: If description is empty after stripping
        """
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Task description cannot be empty")
        return trimmed


class TaskResponse(BaseModel):
    """
    Task response schema.

    Returns complete task data including timestamps.
    """

    id: int
    description: str
    is_complete: bool
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True  # Allows creation from SQLModel objects


class TaskListResponse(BaseModel):
    """
    Task list response schema.

    Returns list of tasks with total count.
    """

    tasks: List[TaskResponse]
    total: int
