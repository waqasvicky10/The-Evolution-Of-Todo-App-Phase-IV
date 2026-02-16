"""
Conversation Message Repository for Phase III

This module implements data access functions for storing and retrieving
conversation messages in the Streamlit SQLite database.

Functions:
    - store_message: Store a new conversation message
    - get_recent_messages: Retrieve recent conversation history
    - get_message_by_id: Retrieve a specific message
    - count_user_messages: Count messages for a user

All functions enforce user data isolation and maintain atomic operations.
"""

import sqlite3
from typing import List, Optional
from datetime import datetime

from phase_iii.persistence.models.conversation import (
    ConversationMessage,
    MessageRole,
    CONVERSATION_MESSAGES_TABLE_SCHEMA
)


# Database path (shared with Phase II Streamlit app)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.environ.get("TODO_DB_PATH"):
    DATABASE_PATH = os.environ.get("TODO_DB_PATH")
elif os.environ.get("VERCEL"):
    DATABASE_PATH = "/tmp/todo.db"
else:
    DATABASE_PATH = os.path.join(BASE_DIR, "todo.db")


def _get_connection() -> sqlite3.Connection:
    """
    Get a database connection with row factory for dict-like access.

    Returns:
        sqlite3.Connection: Database connection

    Internal function - not part of public API.
    """
    conn = sqlite3.connect(DATABASE_PATH, timeout=20)
    conn.row_factory = sqlite3.Row
    return conn


def init_conversation_tables() -> None:
    """
    Initialize conversation tables in the database.

    Creates conversation_messages table if it doesn't exist.
    Safe to call multiple times (CREATE TABLE IF NOT EXISTS).

    This function should be called during application startup.

    Raises:
        sqlite3.Error: If database operation fails

    Example:
        >>> init_conversation_tables()
        # Tables created successfully
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.executescript(CONVERSATION_MESSAGES_TABLE_SCHEMA)
        conn.commit()
    finally:
        conn.close()


def store_message(
    user_id: int,
    role: MessageRole,
    content: str
) -> ConversationMessage:
    """
    Store a new conversation message in the database.

    This function creates a new message record with the provided data,
    generates a unique ID and timestamp, and stores it atomically in
    the database.

    Args:
        user_id: ID of the authenticated user (foreign key to users table)
        role: Message role (USER or ASSISTANT)
        content: Text content of the message

    Returns:
        ConversationMessage: The created message with ID and timestamp

    Raises:
        ValueError: If validation fails (empty content, invalid user_id)
        sqlite3.Error: If database operation fails

    Example:
        >>> msg = store_message(
        ...     user_id=1,
        ...     role=MessageRole.USER,
        ...     content="Add a task to buy groceries"
        ... )
        >>> print(f"Message ID: {msg.id}")
        Message ID: 42

    References:
        - PHASE_III_SPECIFICATION.md: Data Requirements - Conversation Messages
        - PHASE_III_PLAN.md: Persistence Layer Responsibilities
    """
    # Validate inputs
    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    if not content or not content.strip():
        raise ValueError("content cannot be empty")

    if not isinstance(role, MessageRole):
        raise ValueError("role must be a MessageRole enum")

    # Generate timestamp
    timestamp = datetime.now().isoformat()

    # Create message object (without ID)
    message = ConversationMessage(
        id=None,
        user_id=user_id,
        role=role,
        content=content,
        timestamp=timestamp
    )

    # Store in database (atomic operation)
    conn = _get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO conversation_messages (user_id, role, content, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, role.value, content, timestamp)
        )

        # Get the generated ID
        message_id = cursor.lastrowid

        conn.commit()

        # Return message with ID
        return ConversationMessage(
            id=message_id,
            user_id=user_id,
            role=role,
            content=content,
            timestamp=timestamp
        )

    except sqlite3.Error as e:
        conn.rollback()
        raise sqlite3.Error(f"Failed to store message: {e}")
    finally:
        conn.close()


def get_recent_messages(
    user_id: int,
    limit: int = 50,
    offset: int = 0
) -> List[ConversationMessage]:
    """
    Retrieve recent conversation messages for a user.

    Messages are returned in chronological order (oldest first).
    Supports pagination via limit and offset parameters.

    Args:
        user_id: ID of the authenticated user
        limit: Maximum number of messages to return (default: 50)
        offset: Number of messages to skip (default: 0)

    Returns:
        List[ConversationMessage]: List of messages in chronological order

    Raises:
        ValueError: If user_id is invalid or limit/offset are negative
        sqlite3.Error: If database operation fails

    Example:
        >>> messages = get_recent_messages(user_id=1, limit=10)
        >>> for msg in messages:
        ...     print(f"{msg.role.value}: {msg.content}")
        user: Add a task to buy groceries
        assistant: I've added "Buy groceries" to your todo list.

    References:
        - PHASE_III_SPECIFICATION.md: Conversation Behavior - Context Awareness
        - PHASE_III_PLAN.md: Conversation History Handling
    """
    # Validate inputs
    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    if limit < 0:
        raise ValueError("limit cannot be negative")

    if offset < 0:
        raise ValueError("offset cannot be negative")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        # Query messages in chronological order
        cursor.execute(
            """
            SELECT id, user_id, role, content, timestamp
            FROM conversation_messages
            WHERE user_id = ?
            ORDER BY timestamp ASC
            LIMIT ? OFFSET ?
            """,
            (user_id, limit, offset)
        )

        rows = cursor.fetchall()

        # Convert rows to ConversationMessage objects
        messages = []
        for row in rows:
            messages.append(ConversationMessage(
                id=row['id'],
                user_id=row['user_id'],
                role=MessageRole(row['role']),
                content=row['content'],
                timestamp=row['timestamp']
            ))

        return messages

    finally:
        conn.close()


def get_message_by_id(message_id: int, user_id: int) -> Optional[ConversationMessage]:
    """
    Retrieve a specific message by ID.

    Enforces user data isolation - only returns message if it belongs
    to the specified user.

    Args:
        message_id: ID of the message to retrieve
        user_id: ID of the authenticated user (for authorization)

    Returns:
        ConversationMessage: The message if found and authorized, None otherwise

    Raises:
        ValueError: If message_id or user_id is invalid
        sqlite3.Error: If database operation fails

    Example:
        >>> msg = get_message_by_id(message_id=42, user_id=1)
        >>> if msg:
        ...     print(msg.content)
        Add a task to buy groceries
    """
    # Validate inputs
    if message_id <= 0:
        raise ValueError("message_id must be a positive integer")

    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, user_id, role, content, timestamp
            FROM conversation_messages
            WHERE id = ? AND user_id = ?
            """,
            (message_id, user_id)
        )

        row = cursor.fetchone()

        if not row:
            return None

        return ConversationMessage(
            id=row['id'],
            user_id=row['user_id'],
            role=MessageRole(row['role']),
            content=row['content'],
            timestamp=row['timestamp']
        )

    finally:
        conn.close()


def count_user_messages(user_id: int) -> int:
    """
    Count total number of messages for a user.

    Args:
        user_id: ID of the authenticated user

    Returns:
        int: Total count of messages

    Raises:
        ValueError: If user_id is invalid
        sqlite3.Error: If database operation fails

    Example:
        >>> count = count_user_messages(user_id=1)
        >>> print(f"User has {count} messages")
        User has 42 messages
    """
    # Validate input
    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) as count
            FROM conversation_messages
            WHERE user_id = ?
            """,
            (user_id,)
        )

        row = cursor.fetchone()
        return row['count'] if row else 0

    finally:
        conn.close()


def get_latest_message(user_id: int) -> Optional[ConversationMessage]:
    """
    Get the most recent message for a user.

    Args:
        user_id: ID of the authenticated user

    Returns:
        ConversationMessage: Latest message if exists, None otherwise

    Raises:
        ValueError: If user_id is invalid
        sqlite3.Error: If database operation fails

    Example:
        >>> msg = get_latest_message(user_id=1)
        >>> if msg:
        ...     print(f"Latest: {msg.content}")
    """
    # Validate input
    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, user_id, role, content, timestamp
            FROM conversation_messages
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        return ConversationMessage(
            id=row['id'],
            user_id=row['user_id'],
            role=MessageRole(row['role']),
            content=row['content'],
            timestamp=row['timestamp']
        )

    finally:
        conn.close()


def delete_user_messages(user_id: int) -> int:
    """
    Delete all messages for a user.

    WARNING: This is a destructive operation. Use with caution.

    Args:
        user_id: ID of the authenticated user

    Returns:
        int: Number of messages deleted

    Raises:
        ValueError: If user_id is invalid
        sqlite3.Error: If database operation fails

    Example:
        >>> deleted_count = delete_user_messages(user_id=1)
        >>> print(f"Deleted {deleted_count} messages")
    """
    # Validate input
    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM conversation_messages
            WHERE user_id = ?
            """,
            (user_id,)
        )

        deleted_count = cursor.rowcount
        conn.commit()

        return deleted_count

    except sqlite3.Error as e:
        conn.rollback()
        raise sqlite3.Error(f"Failed to delete messages: {e}")
    finally:
        conn.close()


def get_messages_by_role(
    user_id: int,
    role: MessageRole,
    limit: int = 50
) -> List[ConversationMessage]:
    """
    Retrieve messages for a user filtered by role.

    Useful for analyzing user inputs or assistant responses separately.

    Args:
        user_id: ID of the authenticated user
        role: Message role to filter by (USER or ASSISTANT)
        limit: Maximum number of messages to return (default: 50)

    Returns:
        List[ConversationMessage]: List of messages with specified role

    Raises:
        ValueError: If inputs are invalid
        sqlite3.Error: If database operation fails

    Example:
        >>> user_messages = get_messages_by_role(user_id=1, role=MessageRole.USER)
        >>> print(f"User sent {len(user_messages)} messages")
    """
    # Validate inputs
    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    if not isinstance(role, MessageRole):
        raise ValueError("role must be a MessageRole enum")

    if limit < 0:
        raise ValueError("limit cannot be negative")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, user_id, role, content, timestamp
            FROM conversation_messages
            WHERE user_id = ? AND role = ?
            ORDER BY timestamp ASC
            LIMIT ?
            """,
            (user_id, role.value, limit)
        )

        rows = cursor.fetchall()

        messages = []
        for row in rows:
            messages.append(ConversationMessage(
                id=row['id'],
                user_id=row['user_id'],
                role=MessageRole(row['role']),
                content=row['content'],
                timestamp=row['timestamp']
            ))

        return messages

    finally:
        conn.close()


def get_conversation_context(
    user_id: int,
    max_messages: int = 20
) -> List[ConversationMessage]:
    """
    Get recent conversation context for agent invocation.

    Retrieves the most recent N messages to provide context for the agent.
    This is the primary function used by the chat API to load context.

    Args:
        user_id: ID of the authenticated user
        max_messages: Maximum context window size (default: 20)

    Returns:
        List[ConversationMessage]: Recent messages in chronological order

    Raises:
        ValueError: If inputs are invalid
        sqlite3.Error: If database operation fails

    Example:
        >>> context = get_conversation_context(user_id=1, max_messages=10)
        >>> for msg in context:
        ...     print(f"{msg.role.value}: {msg.content}")

    References:
        - PHASE_III_PLAN.md: Conversation History Handling
        - Used by Chat API in Task 4.2
    """
    return get_recent_messages(user_id=user_id, limit=max_messages, offset=0)


def has_conversation_history(user_id: int) -> bool:
    """
    Check if a user has any conversation history.

    Fast check without retrieving full message data.

    Args:
        user_id: ID of the authenticated user

    Returns:
        bool: True if user has messages, False otherwise

    Raises:
        ValueError: If user_id is invalid
        sqlite3.Error: If database operation fails

    Example:
        >>> if has_conversation_history(user_id=1):
        ...     print("Returning user")
        ... else:
        ...     print("New user")
    """
    count = count_user_messages(user_id)
    return count > 0
