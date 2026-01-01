"""
Task database model.

Defines the Task entity with SQLModel for database operations.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class Task(SQLModel, table=True):
    """
    Task model representing todo items in the system.

    Each task belongs to exactly one user (user_id foreign key).

    Attributes:
        id: Auto-incrementing primary key
        description: Task description (1-500 characters)
        is_complete: Task completion status (defaults to False)
        user_id: Foreign key to users table (indexed)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        user: Relationship to the task's owner
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(max_length=500, min_length=1)
    is_complete: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: "User" = Relationship(back_populates="tasks")

    def __repr__(self) -> str:
        """String representation of Task."""
        return f"<Task(id={self.id}, user_id={self.user_id}, complete={self.is_complete})>"
