"""
User database model.

Defines the User entity with SQLModel for database operations.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task


class User(SQLModel, table=True):
    """
    User model representing registered users in the system.

    Attributes:
        id: Auto-incrementing primary key
        email: Unique email address for login (indexed)
        hashed_password: Bcrypt-hashed password (never store plaintext)
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
        tasks: Relationship to user's tasks
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="user")

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, email={self.email})>"
