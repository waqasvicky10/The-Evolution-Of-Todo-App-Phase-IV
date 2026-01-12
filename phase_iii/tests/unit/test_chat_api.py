"""
Unit Tests for Chat API

This module contains unit tests for the FastAPI chat endpoint,
including schemas, routes, and request/response handling.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient

from phase_iii.chat_api.schemas.chat_schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationHistoryResponse,
    ToolCall
)


class TestChatSchemas:
    """Test Pydantic schemas for chat API."""

    def test_chat_message_request_valid(self):
        """Test valid chat message request."""
        request = ChatMessageRequest(message="Add a task to buy groceries")

        assert request.message == "Add a task to buy groceries"

    def test_chat_message_request_empty(self):
        """Test that empty message is rejected."""
        with pytest.raises(ValueError):
            ChatMessageRequest(message="")

    def test_chat_message_response(self):
        """Test chat message response schema."""
        response = ChatMessageResponse(
            response="I've added the task!",
            tool_calls=[],
            timestamp="2026-01-06T10:30:00"
        )

        assert response.response == "I've added the task!"
        assert response.tool_calls == []
        assert response.timestamp == "2026-01-06T10:30:00"

    def test_tool_call_schema(self):
        """Test tool call schema."""
        tool_call = ToolCall(
            tool_name="create_todo",
            parameters={"user_id": 1, "title": "Test"},
            result={"success": True},
            status="success"
        )

        assert tool_call.tool_name == "create_todo"
        assert tool_call.parameters["user_id"] == 1
        assert tool_call.result["success"] is True

    def test_conversation_history_response(self):
        """Test conversation history response schema."""
        response = ConversationHistoryResponse(
            messages=[
                {
                    "role": "user",
                    "content": "Hello",
                    "timestamp": "2026-01-06T10:30:00"
                }
            ],
            count=1
        )

        assert response.count == 1
        assert len(response.messages) == 1
        assert response.messages[0].role == "user"


class TestChatEndpoints:
    """Test chat API endpoints."""

    @pytest.fixture
    def mock_app(self):
        """Create test client with mocked dependencies."""
        from phase_iii.chat_api.main import app

        # No external AI API keys needed for Mock Logic
        yield TestClient(app)

    def test_root_endpoint(self, mock_app):
        """Test root endpoint."""
        response = mock_app.get("/")

        assert response.status_code == 200
        assert "message" in response.json()
        assert "version" in response.json()

    def test_health_endpoint(self, mock_app):
        """Test health check endpoint."""
        response = mock_app.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_chat_health_endpoint(self, mock_app):
        """Test chat health endpoint."""
        response = mock_app.get("/api/chat/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    @patch('phase_iii.chat_api.routes.chat.get_conversation_context')
    @patch('phase_iii.chat_api.routes.chat.store_message')
    @patch('phase_iii.chat_api.routes.chat.create_agent')
    def test_chat_endpoint_unauthorized(
        self,
        mock_create_agent,
        mock_store_message,
        mock_get_context,
        mock_app
    ):
        """Test chat endpoint without authentication."""
        response = mock_app.post(
            "/api/chat",
            json={"message": "Hello"}
        )

        assert response.status_code == 401  # No auth header

    @patch('phase_iii.chat_api.routes.chat.get_conversation_context')
    @patch('phase_iii.chat_api.routes.chat.store_message')
    @patch('phase_iii.chat_api.routes.chat.create_agent')
    def test_chat_endpoint_with_auth(
        self,
        mock_create_agent,
        mock_store_message,
        mock_get_context,
        mock_app
    ):
        """Test chat endpoint with authentication."""
        # Mock conversation context
        mock_get_context.return_value = []

        # Mock store_message
        mock_message = Mock()
        mock_message.id = 1
        mock_message.role = Mock(value="user")
        mock_message.content = "Hello"
        mock_store_message.return_value = mock_message

        # Mock agent
        mock_agent = Mock()
        mock_agent.process_message = Mock(return_value={
            "response_text": "Hi there!",
            "tool_calls": [],
            "requires_tool_execution": False
        })
        mock_create_agent.return_value = mock_agent

        response = mock_app.post(
            "/api/chat",
            json={"message": "Hello"},
            headers={"Authorization": "Bearer test_token"}
        )

        assert response.status_code == 200
        assert "response" in response.json()
        assert response.json()["response"] == "Hi there!"

    def test_chat_history_unauthorized(self, mock_app):
        """Test chat history without authentication."""
        response = mock_app.get("/api/chat/history")

        assert response.status_code == 401

    @patch('phase_iii.chat_api.routes.chat.get_recent_messages')
    def test_chat_history_with_auth(self, mock_get_messages, mock_app):
        """Test chat history with authentication."""
        # Mock message retrieval
        mock_message = Mock()
        mock_message.role = Mock(value="user")
        mock_message.content = "Hello"
        mock_message.timestamp = "2026-01-06T10:30:00"
        mock_get_messages.return_value = [mock_message]

        response = mock_app.get(
            "/api/chat/history",
            headers={"Authorization": "Bearer test_token"}
        )

        assert response.status_code == 200
        assert "messages" in response.json()
        assert response.json()["count"] == 1


class TestToolCallRouting:
    """Test tool call routing to MCP server."""

    @pytest.mark.asyncio
    async def test_execute_tool_calls_success(self):
        """Test successful tool execution."""
        from phase_iii.chat_api.routes.chat import execute_tool_calls

        with patch('phase_iii.chat_api.routes.chat.TOOL_MAP') as mock_tools:
            # Mock tool function
            mock_tool = AsyncMock(return_value={"success": True, "todo_id": 123})
            mock_tools.__getitem__.return_value = mock_tool
            mock_tools.__contains__.return_value = True

            tool_calls = [
                {
                    "name": "create_todo",
                    "tool_use_id": "test_id_1",
                    "input": {"title": "Test task"}
                }
            ]

            results = await execute_tool_calls(tool_calls, user_id=1)

            assert len(results) == 1
            assert results[0]["success"] is True
            assert results[0]["content"]["todo_id"] == 123

    @pytest.mark.asyncio
    async def test_execute_tool_calls_unknown_tool(self):
        """Test handling unknown tool."""
        from phase_iii.chat_api.routes.chat import execute_tool_calls

        with patch('phase_iii.chat_api.routes.chat.TOOL_MAP') as mock_tools:
            mock_tools.__contains__.return_value = False

            tool_calls = [
                {
                    "name": "unknown_tool",
                    "tool_use_id": "test_id_1",
                    "input": {}
                }
            ]

            results = await execute_tool_calls(tool_calls, user_id=1)

            assert len(results) == 1
            assert results[0]["success"] is False
            assert "Unknown tool" in results[0]["content"]["error"]

    @pytest.mark.asyncio
    async def test_execute_tool_calls_error_handling(self):
        """Test tool execution error handling."""
        from phase_iii.chat_api.routes.chat import execute_tool_calls

        with patch('phase_iii.chat_api.routes.chat.TOOL_MAP') as mock_tools:
            # Mock tool that raises exception
            mock_tool = AsyncMock(side_effect=Exception("Tool error"))
            mock_tools.__getitem__.return_value = mock_tool
            mock_tools.__contains__.return_value = True

            tool_calls = [
                {
                    "name": "create_todo",
                    "tool_use_id": "test_id_1",
                    "input": {"title": "Test"}
                }
            ]

            results = await execute_tool_calls(tool_calls, user_id=1)

            assert len(results) == 1
            assert results[0]["success"] is False
            assert "error" in results[0]["content"]


def run_unit_tests():
    """Run all chat API unit tests."""
    print("=" * 60)
    print("CHAT API UNIT TESTS")
    print("=" * 60)
    print()

    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short"
    ])

    return exit_code == 0


if __name__ == "__main__":
    success = run_unit_tests()
    exit(0 if success else 1)
