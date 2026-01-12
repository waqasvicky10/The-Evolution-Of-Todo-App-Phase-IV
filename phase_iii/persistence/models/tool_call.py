"""
Tool Call Record Model for Phase III

This module defines the data schema for storing tool call records
made by the AI agent during conversations. Tool calls are logged for
audit, debugging, and ensuring deterministic behavior.

Schema Design:
- Links to conversation messages
- Stores structured parameters and results (JSON)
- Tracks execution status (success/failure)
- Enables conversation replay and debugging
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any, Dict, List
from enum import Enum
import json


class ToolCallStatus(str, Enum):
    """
    Enumeration of tool call execution statuses.

    Status Values:
        SUCCESS: Tool executed successfully and returned valid result
        FAILURE: Tool execution failed or returned error
        PENDING: Tool call initiated but not yet completed (for async operations)
    """
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"


@dataclass
class ToolCallRecord:
    """
    Data model for a tool call record.

    This schema represents a single tool invocation by the AI agent.
    Tool calls are linked to conversation messages and store all relevant
    information for audit, debugging, and replay.

    Attributes:
        id (int): Unique identifier for the tool call (auto-generated)
        message_id (int): Foreign key to conversation_messages table
        tool_name (str): Name of the MCP tool that was invoked
        parameters (dict): Tool input parameters as structured data (JSON)
        result (dict): Tool output/result as structured data (JSON)
        status (ToolCallStatus): Execution status (success/failure/pending)
        timestamp (str): ISO8601 formatted timestamp of tool invocation
        error_message (str, optional): Error details if status is FAILURE

    Database Schema:
        CREATE TABLE tool_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            tool_name TEXT NOT NULL,
            parameters TEXT NOT NULL,  -- JSON string
            result TEXT,                -- JSON string (nullable for pending)
            status TEXT NOT NULL CHECK(status IN ('success', 'failure', 'pending')),
            timestamp TEXT NOT NULL,
            error_message TEXT,
            FOREIGN KEY (message_id) REFERENCES conversation_messages(id) ON DELETE CASCADE
        );

        CREATE INDEX idx_tool_calls_message_id ON tool_calls(message_id);
        CREATE INDEX idx_tool_calls_tool_name ON tool_calls(tool_name);
        CREATE INDEX idx_tool_calls_timestamp ON tool_calls(timestamp);

    Example:
        >>> tool_call = ToolCallRecord(
        ...     id=1,
        ...     message_id=42,
        ...     tool_name="create_todo",
        ...     parameters={"title": "Buy groceries", "user_id": 1},
        ...     result={"success": True, "todo_id": 123},
        ...     status=ToolCallStatus.SUCCESS,
        ...     timestamp="2026-01-06T10:30:00.123456",
        ...     error_message=None
        ... )
        >>> print(tool_call.tool_name)
        create_todo

    References:
        - PHASE_III_SPECIFICATION.md: Data Requirements - Tool Call Records
        - PHASE_III_PLAN.md: Persistence Strategy, MCP Design
    """

    id: Optional[int]  # None when creating new record, set after insert
    message_id: int  # Links to conversation_messages table
    tool_name: str  # MCP tool name (e.g., "create_todo", "list_todos")
    parameters: Dict[str, Any]  # Tool input parameters (stored as JSON)
    result: Optional[Dict[str, Any]]  # Tool output (stored as JSON, None if pending)
    status: ToolCallStatus  # SUCCESS, FAILURE, or PENDING
    timestamp: str  # ISO8601 format: YYYY-MM-DDTHH:MM:SS.ffffff
    error_message: Optional[str] = None  # Error details if status is FAILURE

    def __post_init__(self):
        """
        Validate tool call data after initialization.

        Ensures:
        - message_id is positive
        - tool_name is non-empty
        - parameters is a dictionary
        - result is a dictionary or None
        - status is valid ToolCallStatus enum
        - timestamp is in ISO8601 format
        - error_message is set only for FAILURE status

        Raises:
            ValueError: If validation fails
        """
        if self.message_id <= 0:
            raise ValueError("message_id must be a positive integer")

        if not self.tool_name or not self.tool_name.strip():
            raise ValueError("tool_name cannot be empty")

        if not isinstance(self.parameters, dict):
            raise ValueError(f"parameters must be a dictionary, got {type(self.parameters)}")

        if self.result is not None and not isinstance(self.result, dict):
            raise ValueError(f"result must be a dictionary or None, got {type(self.result)}")

        if not isinstance(self.status, ToolCallStatus):
            raise ValueError(f"status must be ToolCallStatus enum, got {type(self.status)}")

        # Validate ISO8601 timestamp format
        if self.timestamp:
            try:
                datetime.fromisoformat(self.timestamp)
            except ValueError:
                raise ValueError(f"timestamp must be ISO8601 format, got: {self.timestamp}")

        # Error message should only be set for FAILURE status
        if self.status != ToolCallStatus.FAILURE and self.error_message:
            raise ValueError("error_message should only be set when status is FAILURE")

    def to_dict(self) -> dict:
        """
        Convert tool call record to dictionary for database storage.

        Parameters and result are serialized to JSON strings for storage.

        Returns:
            dict: Dictionary representation with all fields

        Example:
            >>> tool_call.to_dict()
            {
                'id': 1,
                'message_id': 42,
                'tool_name': 'create_todo',
                'parameters': '{"title": "Buy groceries", "user_id": 1}',
                'result': '{"success": true, "todo_id": 123}',
                'status': 'success',
                'timestamp': '2026-01-06T10:30:00.123456',
                'error_message': None
            }
        """
        return {
            'id': self.id,
            'message_id': self.message_id,
            'tool_name': self.tool_name,
            'parameters': json.dumps(self.parameters),
            'result': json.dumps(self.result) if self.result is not None else None,
            'status': self.status.value,
            'timestamp': self.timestamp,
            'error_message': self.error_message
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ToolCallRecord':
        """
        Create tool call record from dictionary (e.g., from database query).

        Parameters and result are deserialized from JSON strings.

        Args:
            data: Dictionary with tool call fields

        Returns:
            ToolCallRecord: New tool call instance

        Example:
            >>> data = {
            ...     'id': 1,
            ...     'message_id': 42,
            ...     'tool_name': 'create_todo',
            ...     'parameters': '{"title": "Buy groceries"}',
            ...     'result': '{"success": true}',
            ...     'status': 'success',
            ...     'timestamp': '2026-01-06T10:30:00.123456',
            ...     'error_message': None
            ... }
            >>> record = ToolCallRecord.from_dict(data)
        """
        return cls(
            id=data.get('id'),
            message_id=data['message_id'],
            tool_name=data['tool_name'],
            parameters=json.loads(data['parameters']),
            result=json.loads(data['result']) if data.get('result') else None,
            status=ToolCallStatus(data['status']),
            timestamp=data['timestamp'],
            error_message=data.get('error_message')
        )

    @staticmethod
    def generate_timestamp() -> str:
        """
        Generate ISO8601 timestamp for current time.

        Returns:
            str: Current timestamp in ISO8601 format with microseconds

        Example:
            >>> timestamp = ToolCallRecord.generate_timestamp()
            >>> print(timestamp)
            '2026-01-06T10:30:00.123456'
        """
        return datetime.now().isoformat()

    def is_success(self) -> bool:
        """Check if tool call was successful."""
        return self.status == ToolCallStatus.SUCCESS

    def is_failure(self) -> bool:
        """Check if tool call failed."""
        return self.status == ToolCallStatus.FAILURE

    def is_pending(self) -> bool:
        """Check if tool call is still pending."""
        return self.status == ToolCallStatus.PENDING

    def get_parameter(self, key: str, default: Any = None) -> Any:
        """
        Get a specific parameter value.

        Args:
            key: Parameter name
            default: Default value if key not found

        Returns:
            Parameter value or default
        """
        return self.parameters.get(key, default)

    def get_result_value(self, key: str, default: Any = None) -> Any:
        """
        Get a specific result value.

        Args:
            key: Result field name
            default: Default value if key not found

        Returns:
            Result value or default
        """
        if self.result is None:
            return default
        return self.result.get(key, default)

    def __repr__(self) -> str:
        """String representation of tool call record."""
        return (
            f"ToolCallRecord(id={self.id}, message_id={self.message_id}, "
            f"tool_name='{self.tool_name}', status={self.status.value}, "
            f"timestamp={self.timestamp})"
        )


# SQL Schema Definition (for reference and database creation)
TOOL_CALLS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS tool_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL,
    tool_name TEXT NOT NULL,
    parameters TEXT NOT NULL,
    result TEXT,
    status TEXT NOT NULL CHECK(status IN ('success', 'failure', 'pending')),
    timestamp TEXT NOT NULL,
    error_message TEXT,
    FOREIGN KEY (message_id) REFERENCES conversation_messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tool_calls_message_id
ON tool_calls(message_id);

CREATE INDEX IF NOT EXISTS idx_tool_calls_tool_name
ON tool_calls(tool_name);

CREATE INDEX IF NOT EXISTS idx_tool_calls_timestamp
ON tool_calls(timestamp);

CREATE INDEX IF NOT EXISTS idx_tool_calls_status
ON tool_calls(status);
"""


# Helper functions for common operations
def serialize_parameters(params: Dict[str, Any]) -> str:
    """
    Serialize parameters to JSON string for storage.

    Args:
        params: Dictionary of parameters

    Returns:
        str: JSON string representation
    """
    return json.dumps(params)


def deserialize_parameters(params_json: str) -> Dict[str, Any]:
    """
    Deserialize parameters from JSON string.

    Args:
        params_json: JSON string

    Returns:
        dict: Deserialized parameters
    """
    return json.loads(params_json)


def serialize_result(result: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Serialize result to JSON string for storage.

    Args:
        result: Dictionary of results or None

    Returns:
        str: JSON string representation or None
    """
    return json.dumps(result) if result is not None else None


def deserialize_result(result_json: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Deserialize result from JSON string.

    Args:
        result_json: JSON string or None

    Returns:
        dict: Deserialized result or None
    """
    return json.loads(result_json) if result_json else None


# Type hints for common operations
ToolCallDict = dict[str, any]
ToolCallList = list[ToolCallRecord]
