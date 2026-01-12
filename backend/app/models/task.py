"""
Task database model.

Defines the Task entity with SQLModel for database operations.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING, List

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
        
        # AI-enhanced fields
        category: AI-determined task category
        priority: AI-determined priority level
        estimated_duration: AI-estimated completion time
        ai_tags: AI-generated tags for organization
        ai_suggestions: AI suggestions for task improvement
        
        user: Relationship to the task's owner
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(max_length=500, min_length=1)
    is_complete: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # AI-enhanced fields
    category: Optional[str] = Field(default=None, max_length=50)
    priority: Optional[str] = Field(default=None, max_length=20)  # high, medium, low
    estimated_duration: Optional[str] = Field(default=None, max_length=50)
    ai_tags: Optional[str] = Field(default=None, max_length=500)  # JSON string of tags
    ai_suggestions: Optional[str] = Field(default=None, max_length=1000)  # JSON string of suggestions

    # Relationship to user
    user: "User" = Relationship(back_populates="tasks")

    def __repr__(self) -> str:
        """String representation of Task."""
        return f"<Task(id={self.id}, user_id={self.user_id}, complete={self.is_complete})>"
