"""
MCP Tool Implementations for Todo Management

This module implements the actual tool handlers that are exposed through
the MCP server. Each tool interfaces with the Phase II Streamlit backend
through the shared SQLite database.

Tools:
    - create_todo: Create a new todo item
    - list_todos: List user's todo items
    - update_todo: Update an existing todo
    - delete_todo: Delete a todo item
    - get_todo: Get a specific todo by ID

All tools are stateless and delegate data operations to the backend.
"""

import logging
import sqlite3
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Database path (shared with Phase II Streamlit app)
# Ensure we use the one in the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Check for Vercel environment to use writable /tmp directory
if os.environ.get("VERCEL"):
    DATABASE_PATH = "/tmp/todo.db"
else:
    DATABASE_PATH = os.path.join(PROJECT_ROOT, "todo.db")


def init_todo_tables():
    """Initialize the tasks table if it doesn't exist."""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                is_complete BOOLEAN DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"Initialized tasks table in {DATABASE_PATH}")
    except Exception as e:
        logger.error(f"Failed to initialize tasks table: {e}")


def _get_connection() -> sqlite3.Connection:
    """
    Get a database connection.

    Returns:
        sqlite3.Connection: Database connection with row factory
    """
    conn = sqlite3.connect(DATABASE_PATH, timeout=20)
    conn.row_factory = sqlite3.Row
    return conn


async def create_todo_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new todo item.

    Args:
        arguments: Tool arguments containing:
            - user_id (int): ID of the authenticated user
            - title (str): Todo item title
            - completed (bool, optional): Initial completion status

    Returns:
        Dict with success status and created todo data

    Example:
        >>> result = await create_todo_tool({
        ...     "user_id": 1,
        ...     "title": "Buy groceries",
        ...     "completed": False
        ... })
        >>> print(result)
        {'success': True, 'todo_id': 123, 'title': 'Buy groceries'}
    """
    user_id = arguments.get("user_id")
    title = arguments.get("title")
    completed = arguments.get("completed", False)

    # Validate inputs
    if not user_id or not isinstance(user_id, int):
        return {"success": False, "error": "Invalid user_id"}

    if not title or not title.strip():
        return {"success": False, "error": "Title cannot be empty"}

    from datetime import datetime
    now = datetime.now().isoformat()

    try:
        conn = _get_connection()
        cursor = conn.cursor()

        # Insert task item
        cursor.execute(
            """
            INSERT INTO tasks (user_id, description, is_complete, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, title.strip(), completed, now, now)
        )

        todo_id = cursor.lastrowid
        conn.commit()
        conn.close()

        logger.info(f"Created task {todo_id} for user {user_id}")

        return {
            "success": True,
            "todo_id": todo_id,
            "title": title.strip(),
            "completed": completed,
            "user_id": user_id
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in create_todo: {e}")
        return {"success": False, "error": str(e)}


async def list_todos_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    List all todo items for a user.

    Args:
        arguments: Tool arguments containing:
            - user_id (int): ID of the authenticated user
            - completed (bool, optional): Filter by completion status

    Returns:
        Dict with success status and list of todos

    Example:
        >>> result = await list_todos_tool({"user_id": 1})
        >>> print(result)
        {'success': True, 'todos': [{'id': 1, 'title': 'Buy groceries', 'completed': False}]}
    """
    user_id = arguments.get("user_id")
    completed_filter = arguments.get("completed")

    # Validate inputs
    if not user_id or not isinstance(user_id, int):
        return {"success": False, "error": "Invalid user_id"}

    try:
        conn = _get_connection()
        cursor = conn.cursor()

        # Build query with optional filter
        if completed_filter is not None:
            cursor.execute(
                """
                SELECT id, description, is_complete
                FROM tasks
                WHERE user_id = ? AND is_complete = ?
                ORDER BY id ASC
                """,
                (user_id, completed_filter)
            )
        else:
            cursor.execute(
                """
                SELECT id, description, is_complete
                FROM tasks
                WHERE user_id = ?
                ORDER BY id ASC
                """,
                (user_id,)
            )

        rows = cursor.fetchall()
        conn.close()

        # Convert rows to dictionaries
        todos = [
            {
                "id": row["id"],
                "title": row["description"],
                "completed": bool(row["is_complete"])
            }
            for row in rows
        ]

        logger.info(f"Listed {len(todos)} todos for user {user_id}")

        return {
            "success": True,
            "todos": todos,
            "count": len(todos)
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in list_todos: {e}")
        return {"success": False, "error": str(e)}


async def update_todo_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing todo item.

    Args:
        arguments: Tool arguments containing:
            - user_id (int): ID of the authenticated user
            - todo_id (int): ID of the todo item to update
            - title (str, optional): New title
            - completed (bool, optional): New completion status

    Returns:
        Dict with success status and updated todo data

    Example:
        >>> result = await update_todo_tool({
        ...     "user_id": 1,
        ...     "todo_id": 123,
        ...     "completed": True
        ... })
    """
    user_id = arguments.get("user_id")
    todo_id = arguments.get("todo_id")
    title = arguments.get("title")
    completed = arguments.get("completed")

    # Validate inputs
    if not user_id or not isinstance(user_id, int):
        return {"success": False, "error": "Invalid user_id"}

    if not todo_id or not isinstance(todo_id, int):
        return {"success": False, "error": "Invalid todo_id"}

    if title is None and completed is None:
        return {"success": False, "error": "No fields to update"}

    try:
        conn = _get_connection()
        cursor = conn.cursor()

        # Check if task exists and belongs to user
        cursor.execute(
            "SELECT id, description, is_complete FROM tasks WHERE id = ? AND user_id = ?",
            (todo_id, user_id)
        )
        existing = cursor.fetchone()

        if not existing:
            conn.close()
            return {"success": False, "error": "Task not found or unauthorized"}

        # Build update query dynamically
        updates = []
        params = []

        if title is not None:
            if not title.strip():
                conn.close()
                return {"success": False, "error": "Description cannot be empty"}
            updates.append("description = ?")
            params.append(title.strip())

        if completed is not None:
            updates.append("is_complete = ?")
            params.append(completed)

        from datetime import datetime
        updates.append("updated_at = ?")
        params.append(datetime.utcnow())

        params.extend([todo_id, user_id])

        cursor.execute(
            f"UPDATE tasks SET {', '.join(updates)} WHERE id = ? AND user_id = ?",
            params
        )

        conn.commit()

        # Fetch updated task
        cursor.execute(
            "SELECT id, description, is_complete FROM tasks WHERE id = ?",
            (todo_id,)
        )
        updated = cursor.fetchone()
        conn.close()

        logger.info(f"Updated task {todo_id} for user {user_id}")

        return {
            "success": True,
            "todo_id": updated["id"],
            "title": updated["description"],
            "completed": bool(updated["is_complete"]),
            "user_id": user_id
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in update_todo: {e}")
        return {"success": False, "error": str(e)}


async def delete_todo_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete a todo item.

    Args:
        arguments: Tool arguments containing:
            - user_id (int): ID of the authenticated user
            - todo_id (int): ID of the todo item to delete

    Returns:
        Dict with success status

    Example:
        >>> result = await delete_todo_tool({
        ...     "user_id": 1,
        ...     "todo_id": 123
        ... })
        >>> print(result)
        {'success': True, 'todo_id': 123}
    """
    user_id = arguments.get("user_id")
    todo_id = arguments.get("todo_id")

    # Validate inputs
    if not user_id or not isinstance(user_id, int):
        return {"success": False, "error": "Invalid user_id"}

    if not todo_id or not isinstance(todo_id, int):
        return {"success": False, "error": "Invalid todo_id"}

    try:
        conn = _get_connection()
        cursor = conn.cursor()

        # Check if task exists and belongs to user
        cursor.execute(
            "SELECT id FROM tasks WHERE id = ? AND user_id = ?",
            (todo_id, user_id)
        )
        existing = cursor.fetchone()

        if not existing:
            conn.close()
            return {"success": False, "error": "Task not found or unauthorized"}

        # Delete task
        cursor.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
            (todo_id, user_id)
        )

        conn.commit()
        conn.close()

        logger.info(f"Deleted task {todo_id} for user {user_id}")

        return {
            "success": True,
            "todo_id": todo_id,
            "deleted": True
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in delete_todo: {e}")
        return {"success": False, "error": str(e)}


async def get_todo_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a specific todo item by ID.

    Args:
        arguments: Tool arguments containing:
            - user_id (int): ID of the authenticated user
            - todo_id (int): ID of the todo item to retrieve

    Returns:
        Dict with success status and todo data

    Example:
        >>> result = await get_todo_tool({
        ...     "user_id": 1,
        ...     "todo_id": 123
        ... })
    """
    user_id = arguments.get("user_id")
    todo_id = arguments.get("todo_id")

    # Validate inputs
    if not user_id or not isinstance(user_id, int):
        return {"success": False, "error": "Invalid user_id"}

    if not todo_id or not isinstance(todo_id, int):
        return {"success": False, "error": "Invalid todo_id"}

    try:
        conn = _get_connection()
        cursor = conn.cursor()

        # Fetch task
        cursor.execute(
            """
            SELECT id, description, is_complete
            FROM tasks
            WHERE id = ? AND user_id = ?
            """,
            (todo_id, user_id)
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            return {"success": False, "error": "Task not found or unauthorized"}

        logger.info(f"Retrieved task {todo_id} for user {user_id}")

        return {
            "success": True,
            "todo": {
                "id": row["id"],
                "title": row["description"],
                "completed": bool(row["is_complete"]),
                "user_id": user_id
            }
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in get_todo: {e}")
        return {"success": False, "error": str(e)}
