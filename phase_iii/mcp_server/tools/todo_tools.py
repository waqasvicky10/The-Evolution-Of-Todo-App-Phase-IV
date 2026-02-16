"""
MCP Tool Implementations for Todo Management

This module implements the actual tool handlers that are exposed through
the MCP server. Each tool interfaces with the Phase II Streamlit backend
through the shared SQLite database.

Tools:
    - create_todo (alias: add_task): Create a new todo item
    - list_todos (alias: list_tasks): List user's todo items
    - update_todo (alias: complete_task, update_task): Update or complete a todo
    - delete_todo (alias: remove_task): Delete a todo item
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


async def get_user_context_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve user context information for personalization.
    
    Args:
        arguments: Tool arguments containing:
            - user_id (int): ID of the authenticated user
            
    Returns:
        Dict with user email, name, and join date
    """
    user_id = arguments.get("user_id")
    if not user_id or not isinstance(user_id, int):
        return {"success": False, "error": "Invalid user_id"}
        
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        
        # In this simplified DB, we only have 'users' table if implemented in Phase II
        # Let's check for users table existence first
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            conn.close()
            # If no users table, return a generic context using common patterns
            return {
                "success": True, 
                "user_id": user_id, 
                "email": f"user{user_id}@example.com",
                "name": f"User {user_id}",
                "message": "User context retrieved (Generic)"
            }
            
        cursor.execute("SELECT email, created_at FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return {"success": False, "error": "User not found"}
            
        return {
            "success": True,
            "user_id": user_id,
            "email": row["email"],
            "name": row["email"].split("@")[0].capitalize(),
            "join_date": row["created_at"],
            "message": "User context retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error in get_user_context: {e}")
        return {"success": False, "error": str(e)}


async def create_todo_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new todo item.

    Args:
        arguments: Tool arguments containing:
            - user_id (int): ID of the authenticated user
            - title (str): Todo item title
            - description (str, optional): Additional description
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
    description = arguments.get("description")
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

        # Prepare the final description
        final_description = title.strip()
        if description and description.strip():
            final_description = f"{final_description} ({description.strip()})"

        # Insert task item
        cursor.execute(
            """
            INSERT INTO tasks (user_id, description, is_complete, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, final_description, completed, now, now)
        )

        todo_id = cursor.lastrowid
        conn.commit()
        conn.close()

        logger.info(f"Created task {todo_id} for user {user_id}")

        return {
            "success": True,
            "todo_id": todo_id,
            "title": title.strip(),
            "description": description.strip() if description else None,
            "complete_title": final_description,
            "completed": completed,
            "user_id": user_id
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in create_todo: {e}")
        return {"success": False, "error": str(e)}

# Alias for create_todo_tool to match the skill requirement
add_task_tool = create_todo_tool


async def list_todos_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    List all todo items for a user with optional filters.

    Args:
        arguments: Tool arguments containing:
            - user_id (int): ID of the authenticated user
            - completed (bool, optional): Filter by completion status
            - status (str, optional): Filter by status string ("all", "pending", "completed")
            - priority (str, optional): Filter by priority ("high", "medium", "low")
            - category (str, optional): Filter by category
            - keyword (str, optional): Search keyword in description

    Returns:
        Dict with success status and list of todos
    """
    user_id = arguments.get("user_id")
    completed_filter = arguments.get("completed")
    status_filter = arguments.get("status", "all")
    priority_filter = arguments.get("priority")
    category_filter = arguments.get("category")
    keyword_filter = arguments.get("keyword")

    # Map status string to completed boolean if status is provided
    if status_filter == "pending":
        completed_filter = False
    elif status_filter == "completed":
        completed_filter = True
    elif status_filter == "all":
        # If explicitly set to all, don't filter by completion unless 'completed' argument is also provided
        pass

    # Validate inputs
    if not user_id or not isinstance(user_id, int):
        return {"success": False, "error": "Invalid user_id"}

    try:
        conn = _get_connection()
        cursor = conn.cursor()

        # Build query dynamically
        query = "SELECT id, description, is_complete, priority, category FROM tasks WHERE user_id = ?"
        params = [user_id]

        if completed_filter is not None:
            query += " AND is_complete = ?"
            params.append(1 if completed_filter else 0)
        
        if priority_filter:
            query += " AND priority = ?"
            params.append(priority_filter)
            
        if category_filter:
            query += " AND category LIKE ?"
            params.append(f"%{category_filter}%")
            
        if keyword_filter:
            query += " AND description LIKE ?"
            params.append(f"%{keyword_filter}%")

        query += " ORDER BY id ASC"
        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        conn.close()

        # Convert rows to dictionaries
        todos = [
            {
                "id": row["id"],
                "title": row["description"],
                "completed": bool(row["is_complete"]),
                "priority": row["priority"],
                "category": row["category"]
            }
            for row in rows
        ]

        logger.info(f"Listed {len(todos)} todos for user {user_id} with filters")

        return {
            "success": True,
            "todos": todos,
            "count": len(todos)
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in list_todos: {e}")
        return {"success": False, "error": str(e)}

# Aliases for list_todos_tool
list_tasks_tool = list_todos_tool
search_tasks_tool = list_todos_tool


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

async def complete_task_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mark a todo item as complete.
    
    This is a specialized wrapper around update_todo_tool.
    
    Args:
        arguments: Tool arguments containing:
            - user_id (int): ID of the authenticated user
            - todo_id (int): ID of the todo item to complete
            
    Returns:
        Dict with success status and updated todo data
    """
    # Simply delegate to update_todo_tool with completed=True
    arguments["completed"] = True
    return await update_todo_tool(arguments)



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

# Aliases for update_todo_tool to match skill requirements
complete_task_tool = complete_task_tool  # Already defined above
update_task_tool = update_todo_tool
remove_task_tool = delete_todo_tool



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
