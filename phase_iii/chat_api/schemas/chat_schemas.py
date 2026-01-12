"""
Chat API Schemas for Phase III

This module defines Pydantic models for chat API request/response validation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ChatMessageRequest(BaseModel):
    """
    Request schema for sending a chat message.

    Attributes:
        message: User's message text
    """
    message: str = Field(..., min_length=1, max_length=5000, description="User message")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Add a task to buy groceries"
            }
        }


class ToolCall(BaseModel):
    """
    Schema for a tool call executed during conversation.

    Attributes:
        tool_name: Name of the tool called
        parameters: Tool parameters
        result: Tool execution result
        status: Execution status
    """
    tool_name: str
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    status: str


class ChatMessageResponse(BaseModel):
    """
    Response schema for chat message.

    Attributes:
        response: Agent's response message
        tool_calls: List of tool calls made (for debugging)
        timestamp: Response timestamp
    """
    response: str
    tool_calls: List[ToolCall] = []
    timestamp: str

    class Config:
        json_schema_extra = {
            "example": {
                "response": "I've added 'Buy groceries' to your todo list!",
                "tool_calls": [
                    {
                        "tool_name": "create_todo",
                        "parameters": {"user_id": 1, "title": "Buy groceries"},
                        "result": {"success": True, "todo_id": 123},
                        "status": "success"
                    }
                ],
                "timestamp": "2026-01-06T10:30:00.123456"
            }
        }


class ConversationMessage(BaseModel):
    """
    Schema for a single conversation message.

    Attributes:
        role: Message role (user or assistant)
        content: Message content
        timestamp: Message timestamp
    """
    role: str
    content: str
    timestamp: str


class ConversationHistoryResponse(BaseModel):
    """
    Response schema for conversation history.

    Attributes:
        messages: List of conversation messages
        count: Total number of messages
    """
    messages: List[ConversationMessage]
    count: int

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "Add a task to buy groceries",
                        "timestamp": "2026-01-06T10:30:00.123456"
                    },
                    {
                        "role": "assistant",
                        "content": "I've added 'Buy groceries' to your todo list!",
                        "timestamp": "2026-01-06T10:30:01.123456"
                    }
                ],
                "count": 2
            }
        }


class ErrorResponse(BaseModel):
    """
    Schema for error responses.

    Attributes:
        error: Error message
        detail: Additional error details (optional)
    """
    error: str
    detail: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Authentication required",
                "detail": "Please log in to access this endpoint"
            }
        }
