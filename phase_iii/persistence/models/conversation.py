"""
Conversation Message Model for Phase III

This module defines the data schema for storing conversation messages
between users and the AI agent in the Phase III chatbot.

Schema Design:
- Stores all user and agent messages
- Links to existing Phase II user accounts
- Uses ISO8601 timestamps for consistency
- Supports retrieval by user and chronological ordering
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal
from enum import Enum


class MessageRole(str, Enum):
    """
    Enumeration of message roles in a conversation.

    Roles:
        USER: Message sent by the authenticated user
        ASSISTANT: Message sent by the AI agent
    """
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class ConversationMessage:
    """
    Data model for a single conversation message.

    This schema represents one message in a conversation between a user
    and the AI agent. Messages are stored in the Streamlit SQLite database
    and support the stateless architecture by externalizing all conversation
    state to persistence.

    Attributes:
        id (int): Unique identifier for the message (auto-generated)
        user_id (int): Foreign key to users table (links to Phase II users)
        role (MessageRole): Whether this is a user or assistant message
        content (str): The actual text content of the message
        timestamp (str): ISO8601 formatted timestamp of message creation

    Database Schema:
        CREATE TABLE conversation_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE INDEX idx_conversation_user_id ON conversation_messages(user_id);
        CREATE INDEX idx_conversation_timestamp ON conversation_messages(timestamp);

    Example:
        >>> msg = ConversationMessage(
        ...     id=1,
        ...     user_id=42,
        ...     role=MessageRole.USER,
        ...     content="Add a task to buy groceries",
        ...     timestamp="2026-01-06T10:30:00.123456"
        ... )
        >>> print(msg.role)
        MessageRole.USER

    References:
        - PHASE_III_SPECIFICATION.md: Data Requirements - Conversation Messages
        - PHASE_III_PLAN.md: Persistence Strategy, Stateless Design
    """

    id: Optional[int]  # None when creating new message, set after insert
    user_id: int  # Links to Phase II users table
    role: MessageRole  # USER or ASSISTANT
    content: str  # Message text content
    timestamp: str  # ISO8601 format: YYYY-MM-DDTHH:MM:SS.ffffff

    def __post_init__(self):
        """
        Validate message data after initialization.

        Ensures:
        - user_id is positive
        - role is valid MessageRole enum
        - content is non-empty
        - timestamp is in ISO8601 format

        Raises:
            ValueError: If validation fails
        """
        if self.user_id <= 0:
            raise ValueError("user_id must be a positive integer")

        if not isinstance(self.role, MessageRole):
            raise ValueError(f"role must be MessageRole enum, got {type(self.role)}")

        if not self.content or not self.content.strip():
            raise ValueError("content cannot be empty")

        # Validate ISO8601 timestamp format
        if self.timestamp:
            try:
                datetime.fromisoformat(self.timestamp)
            except ValueError:
                raise ValueError(f"timestamp must be ISO8601 format, got: {self.timestamp}")

    def to_dict(self) -> dict:
        """
        Convert message to dictionary for database storage.

        Returns:
            dict: Dictionary representation with all fields

        Example:
            >>> msg.to_dict()
            {
                'id': 1,
                'user_id': 42,
                'role': 'user',
                'content': 'Add a task to buy groceries',
                'timestamp': '2026-01-06T10:30:00.123456'
            }
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role': self.role.value,
            'content': self.content,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ConversationMessage':
        """
        Create message from dictionary (e.g., from database query).

        Args:
            data: Dictionary with message fields

        Returns:
            ConversationMessage: New message instance

        Example:
            >>> data = {
            ...     'id': 1,
            ...     'user_id': 42,
            ...     'role': 'user',
            ...     'content': 'Add a task',
            ...     'timestamp': '2026-01-06T10:30:00.123456'
            ... }
            >>> msg = ConversationMessage.from_dict(data)
        """
        return cls(
            id=data.get('id'),
            user_id=data['user_id'],
            role=MessageRole(data['role']),
            content=data['content'],
            timestamp=data['timestamp']
        )

    @staticmethod
    def generate_timestamp() -> str:
        """
        Generate ISO8601 timestamp for current time.

        Returns:
            str: Current timestamp in ISO8601 format with microseconds

        Example:
            >>> timestamp = ConversationMessage.generate_timestamp()
            >>> print(timestamp)
            '2026-01-06T10:30:00.123456'
        """
        return datetime.now().isoformat()

    def is_user_message(self) -> bool:
        """Check if this is a user message."""
        return self.role == MessageRole.USER

    def is_assistant_message(self) -> bool:
        """Check if this is an assistant message."""
        return self.role == MessageRole.ASSISTANT

    def __repr__(self) -> str:
        """String representation of message."""
        return (
            f"ConversationMessage(id={self.id}, user_id={self.user_id}, "
            f"role={self.role.value}, content='{self.content[:50]}...', "
            f"timestamp={self.timestamp})"
        )


# SQL Schema Definition (for reference and database creation)
CONVERSATION_MESSAGES_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS conversation_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_conversation_user_id
ON conversation_messages(user_id);

CREATE INDEX IF NOT EXISTS idx_conversation_timestamp
ON conversation_messages(timestamp);

CREATE INDEX IF NOT EXISTS idx_conversation_user_timestamp
ON conversation_messages(user_id, timestamp DESC);
"""


# Type hints for common operations
MessageDict = dict[str, any]
MessageList = list[ConversationMessage]
