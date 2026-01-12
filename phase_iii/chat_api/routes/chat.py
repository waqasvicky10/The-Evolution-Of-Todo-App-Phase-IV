"""
Chat API Routes for Phase III

This module implements the FastAPI endpoints for chat interactions.
"""

import logging
import os
from typing import Dict, Any, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from phase_iii.chat_api.schemas.chat_schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationHistoryResponse,
    ErrorResponse,
    ToolCall
)

from phase_iii.agent import create_agent, get_mcp_tool_definitions
from phase_iii.agent.config.agent_config import get_agent_config

from phase_iii.persistence.repositories.conversation_repo import (
    store_message,
    get_recent_messages,
    get_conversation_context
)
from phase_iii.persistence.repositories.tool_call_repo import (
    store_tool_call
)
from phase_iii.persistence.models.conversation import MessageRole
from phase_iii.persistence.models.tool_call import ToolCallStatus

from phase_iii.mcp_server.tools.todo_tools import (
    create_todo_tool,
    list_todos_tool,
    update_todo_tool,
    delete_todo_tool,
    get_todo_tool
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])
security = HTTPBearer()


# Tool routing map
TOOL_MAP = {
    "create_todo": create_todo_tool,
    "list_todos": list_todos_tool,
    "update_todo": update_todo_tool,
    "delete_todo": delete_todo_tool,
    "get_todo": get_todo_tool
}


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    Extract user ID from authentication credentials.

    For now, this is a simplified implementation. In production, this would:
    - Validate the JWT token
    - Extract user_id from token claims
    - Verify token hasn't expired
    - Check user exists in database

    Args:
        credentials: HTTP Bearer token

    Returns:
        User ID

    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials

    # Simple validation for demo purposes
    if token == "test_token":
        return 1
    
    if token.isdigit():
        return int(token)

    # Try to decode JWT to get user_id
    try:
        import jwt
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload.get("user_id")
        if user_id:
            return int(user_id)
    except Exception as e:
        logger.error(f"Failed to decode token: {e}")

    # Fallback to 1 for demo if all else fails
    logger.warning(f"Using fallback user_id 1 for token starting with: {token[:20]}...")
    return 1


@router.post("/chat", response_model=ChatMessageResponse)
async def chat(
    request: ChatMessageRequest,
    user_id: int = Depends(get_current_user_id)
) -> ChatMessageResponse:
    """
    Process a chat message and return agent response.

    This endpoint:
    1. Retrieves conversation history
    2. Stores user message
    3. Invokes AI agent
    4. Executes tool calls if needed
    5. Stores agent response and tool calls
    6. Returns final response

    Args:
        request: Chat message request
        user_id: Authenticated user ID (from token)

    Returns:
        Agent response with tool calls

    Raises:
        HTTPException: For various error conditions
    """
    try:
        logger.info(f"Chat request from user {user_id}: {request.message[:50]}...")

        # Step 1: Retrieve conversation history
        conversation_history = get_conversation_context(
            user_id=user_id,
            max_messages=20
        )

        # Convert to agent format
        history_messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in conversation_history
        ]

        logger.info(f"Retrieved {len(history_messages)} messages from history")

        # Step 2: Store user message
        user_msg = store_message(
            user_id=user_id,
            role=MessageRole.USER,
            content=request.message
        )

        logger.info(f"Stored user message with ID: {user_msg.id}")

        # Step 3: Get AI agent
        agent = create_agent(api_key="mock", config=get_agent_config())
        tools = get_mcp_tool_definitions()

        # Step 4: Invoke agent
        logger.info("Invoking AI agent...")
        agent_response = agent.process_message(
            user_message=request.message,
            conversation_history=history_messages,
            user_id=user_id,
            tools=tools
        )

        logger.info(f"Agent response: {agent_response.get('requires_tool_execution')}")

        # Step 5: Execute tool calls if needed
        tool_call_records = []
        final_response_text = agent_response["response_text"]

        if agent_response.get("requires_tool_execution"):
            logger.info(f"Executing {len(agent_response['tool_calls'])} tool calls")

            # Execute tools
            tool_results = await execute_tool_calls(
                agent_response["tool_calls"],
                user_id
            )

            # Store assistant message with initial response (if any)
            # (Claude often sends thoughts or "I'll do that" first)
            assistant_msg_initial = store_message(
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                content=final_response_text or "Processing..."
            )

            # Store tool call records and execute them
            for tool_call, result in zip(agent_response["tool_calls"], tool_results):
                store_tool_call(
                    message_id=assistant_msg_initial.id,
                    tool_name=tool_call["name"],
                    parameters=tool_call["input"],
                    result=result["content"],
                    status=ToolCallStatus.SUCCESS if result.get("success", True) else ToolCallStatus.FAILURE
                )

                tool_call_records.append(ToolCall(
                    tool_name=tool_call["name"],
                    parameters=tool_call["input"],
                    result=result["content"],
                    status="success" if result.get("success", True) else "failure"
                ))

            # Step 11: Get final conversational response from agent with tool results
            logger.info("Getting final response with tool results...")
            
            # Use the mock agent to summarize
            agent_final = agent.process_tool_results(
                tool_results=tool_results,
                user_id=user_id
            )
            final_response_text = agent_final["response_text"]
            
            # Store the final conversational response
            store_message(
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                content=final_response_text
            )

        else:
            # No tool calls, just store assistant response
            assistant_msg = store_message(
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                content=final_response_text
            )

        logger.info("Chat processing complete")

        return ChatMessageResponse(
            response=final_response_text,
            tool_calls=tool_call_records,
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred processing your message. Please try again."
        )


async def execute_tool_calls(
    tool_calls: List[Dict[str, Any]],
    user_id: int
) -> List[Dict[str, Any]]:
    """
    Execute a list of tool calls via MCP server.

    Args:
        tool_calls: List of tool calls from agent
        user_id: User ID for context

    Returns:
        List of tool results
    """
    results = []

    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        parameters = tool_call["input"]

        # Ensure user_id is in parameters
        parameters["user_id"] = user_id

        logger.info(f"Executing tool: {tool_name}")

        try:
            # Route to appropriate tool
            if tool_name in TOOL_MAP:
                tool_function = TOOL_MAP[tool_name]
                result = await tool_function(parameters)

                results.append({
                    "tool_use_id": tool_call["tool_use_id"],
                    "content": result,
                    "success": result.get("success", True)
                })
            else:
                logger.error(f"Unknown tool: {tool_name}")
                results.append({
                    "tool_use_id": tool_call["tool_use_id"],
                    "content": {"success": False, "error": f"Unknown tool: {tool_name}"},
                    "success": False
                })

        except Exception as e:
            logger.error(f"Tool execution error: {e}", exc_info=True)
            results.append({
                "tool_use_id": tool_call["tool_use_id"],
                "content": {"success": False, "error": str(e)},
                "success": False
            })

    return results


@router.get("/chat/history", response_model=ConversationHistoryResponse)
async def get_chat_history(
    user_id: int = Depends(get_current_user_id),
    limit: int = 50
) -> ConversationHistoryResponse:
    """
    Retrieve conversation history for the authenticated user.

    Args:
        user_id: Authenticated user ID
        limit: Maximum number of messages to retrieve

    Returns:
        Conversation history
    """
    try:
        logger.info(f"Retrieving chat history for user {user_id}")

        messages = get_recent_messages(user_id=user_id, limit=limit)

        history_messages = [
            {
                "role": msg.role.value,
                "content": msg.content,
                "timestamp": msg.timestamp
            }
            for msg in messages
        ]

        return ConversationHistoryResponse(
            messages=history_messages,
            count=len(history_messages)
        )

    except Exception as e:
        logger.error(f"Error retrieving history: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving conversation history"
        )


@router.get("/chat/health")
async def health_check():
    """Health check endpoint for chat API."""
    return {
        "status": "healthy",
        "service": "chat_api",
        "version": "1.0.0"
    }
