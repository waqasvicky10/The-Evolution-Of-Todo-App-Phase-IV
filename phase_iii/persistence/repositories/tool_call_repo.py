"""
Tool Call Record Repository for Phase III

This module implements data access functions for storing and retrieving
tool call records in the Streamlit SQLite database.

Functions:
    - store_tool_call: Store a new tool call record
    - get_tool_calls_by_message: Retrieve tool calls for a message
    - get_tool_call_by_id: Retrieve a specific tool call
    - get_recent_tool_calls: Retrieve recent tool calls for a user

All functions maintain data integrity and support audit/debugging.
"""

import sqlite3
from typing import List, Optional, Dict, Any
from datetime import datetime

from phase_iii.persistence.models.tool_call import (
    ToolCallRecord,
    ToolCallStatus,
    TOOL_CALLS_TABLE_SCHEMA
)


# Database path (shared with Phase II Streamlit app)
DATABASE_PATH = "todo.db"


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


def init_tool_call_tables() -> None:
    """
    Initialize tool call tables in the database.

    Creates tool_calls table if it doesn't exist.
    Safe to call multiple times (CREATE TABLE IF NOT EXISTS).

    This function should be called during application startup.

    Raises:
        sqlite3.Error: If database operation fails

    Example:
        >>> init_tool_call_tables()
        # Tables created successfully
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.executescript(TOOL_CALLS_TABLE_SCHEMA)
        conn.commit()
    finally:
        conn.close()


def store_tool_call(
    message_id: int,
    tool_name: str,
    parameters: Dict[str, Any],
    result: Optional[Dict[str, Any]] = None,
    status: ToolCallStatus = ToolCallStatus.SUCCESS,
    error_message: Optional[str] = None
) -> ToolCallRecord:
    """
    Store a new tool call record in the database.

    This function creates a new tool call record with the provided data,
    generates a unique ID and timestamp, serializes parameters and result
    to JSON, and stores it atomically in the database.

    Args:
        message_id: ID of the conversation message this tool call belongs to
        tool_name: Name of the MCP tool that was invoked
        parameters: Tool input parameters (will be serialized to JSON)
        result: Tool output result (will be serialized to JSON, optional)
        status: Execution status (SUCCESS, FAILURE, or PENDING)
        error_message: Error details if status is FAILURE (optional)

    Returns:
        ToolCallRecord: The created tool call record with ID and timestamp

    Raises:
        ValueError: If validation fails
        sqlite3.Error: If database operation fails

    Example:
        >>> tool_call = store_tool_call(
        ...     message_id=42,
        ...     tool_name="create_todo",
        ...     parameters={"title": "Buy groceries", "user_id": 1},
        ...     result={"success": True, "todo_id": 123},
        ...     status=ToolCallStatus.SUCCESS
        ... )
        >>> print(f"Tool call ID: {tool_call.id}")
        Tool call ID: 1

    References:
        - PHASE_III_SPECIFICATION.md: Data Requirements - Tool Call Records
        - PHASE_III_PLAN.md: MCP Design, Tool Call Recording
    """
    # Validate inputs
    if message_id <= 0:
        raise ValueError("message_id must be a positive integer")

    if not tool_name or not tool_name.strip():
        raise ValueError("tool_name cannot be empty")

    if not isinstance(parameters, dict):
        raise ValueError("parameters must be a dictionary")

    if result is not None and not isinstance(result, dict):
        raise ValueError("result must be a dictionary or None")

    if not isinstance(status, ToolCallStatus):
        raise ValueError("status must be a ToolCallStatus enum")

    if status != ToolCallStatus.FAILURE and error_message:
        raise ValueError("error_message should only be set when status is FAILURE")

    # Generate timestamp
    timestamp = datetime.now().isoformat()

    # Create tool call record object (without ID)
    tool_call = ToolCallRecord(
        id=None,
        message_id=message_id,
        tool_name=tool_name,
        parameters=parameters,
        result=result,
        status=status,
        timestamp=timestamp,
        error_message=error_message
    )

    # Convert to dict for storage (includes JSON serialization)
    tool_call_dict = tool_call.to_dict()

    # Store in database (atomic operation)
    conn = _get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tool_calls
            (message_id, tool_name, parameters, result, status, timestamp, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tool_call_dict['message_id'],
                tool_call_dict['tool_name'],
                tool_call_dict['parameters'],
                tool_call_dict['result'],
                tool_call_dict['status'],
                tool_call_dict['timestamp'],
                tool_call_dict['error_message']
            )
        )

        # Get the generated ID
        tool_call_id = cursor.lastrowid

        conn.commit()

        # Return tool call with ID
        return ToolCallRecord(
            id=tool_call_id,
            message_id=message_id,
            tool_name=tool_name,
            parameters=parameters,
            result=result,
            status=status,
            timestamp=timestamp,
            error_message=error_message
        )

    except sqlite3.Error as e:
        conn.rollback()
        raise sqlite3.Error(f"Failed to store tool call: {e}")
    finally:
        conn.close()


def get_tool_calls_by_message(message_id: int) -> List[ToolCallRecord]:
    """
    Retrieve all tool calls associated with a message.

    Returns tool calls in chronological order (order they were executed).

    Args:
        message_id: ID of the conversation message

    Returns:
        List[ToolCallRecord]: List of tool calls for the message

    Raises:
        ValueError: If message_id is invalid
        sqlite3.Error: If database operation fails

    Example:
        >>> tool_calls = get_tool_calls_by_message(message_id=42)
        >>> for tc in tool_calls:
        ...     print(f"{tc.tool_name}: {tc.status.value}")
        create_todo: success
    """
    # Validate input
    if message_id <= 0:
        raise ValueError("message_id must be a positive integer")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, message_id, tool_name, parameters, result,
                   status, timestamp, error_message
            FROM tool_calls
            WHERE message_id = ?
            ORDER BY timestamp ASC
            """,
            (message_id,)
        )

        rows = cursor.fetchall()

        # Convert rows to ToolCallRecord objects
        tool_calls = []
        for row in rows:
            tool_call_dict = {
                'id': row['id'],
                'message_id': row['message_id'],
                'tool_name': row['tool_name'],
                'parameters': row['parameters'],
                'result': row['result'],
                'status': row['status'],
                'timestamp': row['timestamp'],
                'error_message': row['error_message']
            }
            tool_calls.append(ToolCallRecord.from_dict(tool_call_dict))

        return tool_calls

    finally:
        conn.close()


def get_tool_call_by_id(tool_call_id: int) -> Optional[ToolCallRecord]:
    """
    Retrieve a specific tool call by ID.

    Args:
        tool_call_id: ID of the tool call to retrieve

    Returns:
        ToolCallRecord: The tool call if found, None otherwise

    Raises:
        ValueError: If tool_call_id is invalid
        sqlite3.Error: If database operation fails

    Example:
        >>> tc = get_tool_call_by_id(tool_call_id=1)
        >>> if tc:
        ...     print(tc.tool_name)
        create_todo
    """
    # Validate input
    if tool_call_id <= 0:
        raise ValueError("tool_call_id must be a positive integer")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, message_id, tool_name, parameters, result,
                   status, timestamp, error_message
            FROM tool_calls
            WHERE id = ?
            """,
            (tool_call_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        tool_call_dict = {
            'id': row['id'],
            'message_id': row['message_id'],
            'tool_name': row['tool_name'],
            'parameters': row['parameters'],
            'result': row['result'],
            'status': row['status'],
            'timestamp': row['timestamp'],
            'error_message': row['error_message']
        }

        return ToolCallRecord.from_dict(tool_call_dict)

    finally:
        conn.close()


def get_recent_tool_calls(
    limit: int = 50,
    tool_name: Optional[str] = None,
    status: Optional[ToolCallStatus] = None
) -> List[ToolCallRecord]:
    """
    Retrieve recent tool calls with optional filtering.

    Useful for debugging, monitoring, and analytics.

    Args:
        limit: Maximum number of tool calls to return (default: 50)
        tool_name: Filter by specific tool name (optional)
        status: Filter by execution status (optional)

    Returns:
        List[ToolCallRecord]: List of tool calls in reverse chronological order

    Raises:
        ValueError: If limit is negative
        sqlite3.Error: If database operation fails

    Example:
        >>> recent = get_recent_tool_calls(limit=10, tool_name="create_todo")
        >>> print(f"Found {len(recent)} recent create_todo calls")
    """
    # Validate input
    if limit < 0:
        raise ValueError("limit cannot be negative")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        # Build query with optional filters
        query = """
            SELECT id, message_id, tool_name, parameters, result,
                   status, timestamp, error_message
            FROM tool_calls
            WHERE 1=1
        """
        params = []

        if tool_name:
            query += " AND tool_name = ?"
            params.append(tool_name)

        if status:
            query += " AND status = ?"
            params.append(status.value)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Convert rows to ToolCallRecord objects
        tool_calls = []
        for row in rows:
            tool_call_dict = {
                'id': row['id'],
                'message_id': row['message_id'],
                'tool_name': row['tool_name'],
                'parameters': row['parameters'],
                'result': row['result'],
                'status': row['status'],
                'timestamp': row['timestamp'],
                'error_message': row['error_message']
            }
            tool_calls.append(ToolCallRecord.from_dict(tool_call_dict))

        return tool_calls

    finally:
        conn.close()


def count_tool_calls(
    tool_name: Optional[str] = None,
    status: Optional[ToolCallStatus] = None
) -> int:
    """
    Count tool calls with optional filtering.

    Args:
        tool_name: Filter by specific tool name (optional)
        status: Filter by execution status (optional)

    Returns:
        int: Total count of tool calls matching filters

    Raises:
        sqlite3.Error: If database operation fails

    Example:
        >>> total = count_tool_calls()
        >>> failures = count_tool_calls(status=ToolCallStatus.FAILURE)
        >>> print(f"{failures} of {total} calls failed")
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()

        # Build query with optional filters
        query = "SELECT COUNT(*) as count FROM tool_calls WHERE 1=1"
        params = []

        if tool_name:
            query += " AND tool_name = ?"
            params.append(tool_name)

        if status:
            query += " AND status = ?"
            params.append(status.value)

        cursor.execute(query, params)
        row = cursor.fetchone()

        return row['count'] if row else 0

    finally:
        conn.close()


def get_tool_call_statistics() -> Dict[str, Any]:
    """
    Get aggregate statistics about tool calls.

    Returns dictionary with counts by tool name and status.

    Returns:
        Dict[str, Any]: Statistics including total, by_tool, by_status

    Raises:
        sqlite3.Error: If database operation fails

    Example:
        >>> stats = get_tool_call_statistics()
        >>> print(f"Total tool calls: {stats['total']}")
        >>> print(f"Success rate: {stats['success_rate']:.1%}")
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()

        # Get total count
        cursor.execute("SELECT COUNT(*) as count FROM tool_calls")
        total = cursor.fetchone()['count']

        # Get counts by tool name
        cursor.execute("""
            SELECT tool_name, COUNT(*) as count
            FROM tool_calls
            GROUP BY tool_name
            ORDER BY count DESC
        """)
        by_tool = {row['tool_name']: row['count'] for row in cursor.fetchall()}

        # Get counts by status
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM tool_calls
            GROUP BY status
        """)
        by_status = {row['status']: row['count'] for row in cursor.fetchall()}

        # Calculate success rate
        success_count = by_status.get('success', 0)
        success_rate = success_count / total if total > 0 else 0

        return {
            'total': total,
            'by_tool': by_tool,
            'by_status': by_status,
            'success_rate': success_rate
        }

    finally:
        conn.close()


def update_tool_call_result(
    tool_call_id: int,
    result: Dict[str, Any],
    status: ToolCallStatus = ToolCallStatus.SUCCESS,
    error_message: Optional[str] = None
) -> bool:
    """
    Update tool call result and status.

    Useful for async operations that complete after initial storage.

    Args:
        tool_call_id: ID of the tool call to update
        result: Tool execution result
        status: Updated execution status
        error_message: Error details if status is FAILURE (optional)

    Returns:
        bool: True if updated successfully, False if not found

    Raises:
        ValueError: If validation fails
        sqlite3.Error: If database operation fails

    Example:
        >>> updated = update_tool_call_result(
        ...     tool_call_id=1,
        ...     result={"success": True, "todo_id": 123},
        ...     status=ToolCallStatus.SUCCESS
        ... )
    """
    # Validate inputs
    if tool_call_id <= 0:
        raise ValueError("tool_call_id must be a positive integer")

    if not isinstance(result, dict):
        raise ValueError("result must be a dictionary")

    if not isinstance(status, ToolCallStatus):
        raise ValueError("status must be a ToolCallStatus enum")

    # Create temporary record for serialization
    import json
    result_json = json.dumps(result)

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE tool_calls
            SET result = ?, status = ?, error_message = ?
            WHERE id = ?
            """,
            (result_json, status.value, error_message, tool_call_id)
        )

        updated = cursor.rowcount > 0
        conn.commit()

        return updated

    except sqlite3.Error as e:
        conn.rollback()
        raise sqlite3.Error(f"Failed to update tool call: {e}")
    finally:
        conn.close()
