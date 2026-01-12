"""
Persistence Models for Phase III

This module exports data models for Phase III conversation and tool call storage.

Models:
    - ConversationMessage: Chat message storage
    - ToolCallRecord: Tool invocation logging

Schemas:
    - CONVERSATION_MESSAGES_TABLE_SCHEMA: SQL for messages table
    - TOOL_CALLS_TABLE_SCHEMA: SQL for tool calls table
"""

from .conversation import (
    ConversationMessage,
    MessageRole,
    MessageDict,
    MessageList,
    CONVERSATION_MESSAGES_TABLE_SCHEMA
)

from .tool_call import (
    ToolCallRecord,
    ToolCallStatus,
    ToolCallDict,
    ToolCallList,
    TOOL_CALLS_TABLE_SCHEMA,
    serialize_parameters,
    deserialize_parameters,
    serialize_result,
    deserialize_result
)

__all__ = [
    # Conversation models
    'ConversationMessage',
    'MessageRole',
    'MessageDict',
    'MessageList',
    'CONVERSATION_MESSAGES_TABLE_SCHEMA',

    # Tool call models
    'ToolCallRecord',
    'ToolCallStatus',
    'ToolCallDict',
    'ToolCallList',
    'TOOL_CALLS_TABLE_SCHEMA',

    # Helper functions
    'serialize_parameters',
    'deserialize_parameters',
    'serialize_result',
    'deserialize_result'
]
