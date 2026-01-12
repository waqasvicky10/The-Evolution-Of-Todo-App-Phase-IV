"""
Unit Tests for MCP Server

This module contains unit tests for the MCP server implementation,
including tool registration, initialization, and basic functionality.

Tests verify:
- Server initialization and lifecycle
- Tool registration
- Health check endpoint
- Stateless operation
- Logging configuration
"""

import pytest
import asyncio
import logging
from unittest.mock import MagicMock, patch

from phase_iii.mcp_server.server import TodoMCPServer, health_check


class TestTodoMCPServer:
    """Test TodoMCPServer initialization and configuration."""

    def test_server_initialization(self):
        """Test that server initializes correctly."""
        server = TodoMCPServer()

        assert server is not None
        assert server.server is not None
        assert server.tools == {}
        assert server.server.name == "todo-mcp-server"

    def test_tool_registration(self):
        """Test that tools are registered correctly."""
        server = TodoMCPServer()
        server.register_tools()

        # Verify all tools registered
        assert "create_todo" in server.tools
        assert "list_todos" in server.tools
        assert "update_todo" in server.tools
        assert "delete_todo" in server.tools
        assert "get_todo" in server.tools

        # Verify correct count
        assert len(server.tools) == 5

    @pytest.mark.asyncio
    async def test_server_start(self):
        """Test server start lifecycle."""
        server = TodoMCPServer()

        await server.start()

        # Verify tools are registered after start
        assert len(server.tools) == 5
        assert "create_todo" in server.tools

    @pytest.mark.asyncio
    async def test_server_stop(self):
        """Test server stop lifecycle."""
        server = TodoMCPServer()
        await server.start()

        # Should not raise exception
        await server.stop()

    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test health check endpoint."""
        status = await health_check()

        assert status["status"] == "healthy"
        assert status["server"] == "todo-mcp-server"
        assert status["version"] == "1.0.0"
        assert status["tools_count"] == 5
        assert status["stateless"] is True

    def test_server_is_stateless(self):
        """Test that server maintains no state."""
        server = TodoMCPServer()

        # Server should have no conversation state
        assert not hasattr(server, 'conversations')
        assert not hasattr(server, 'sessions')
        assert not hasattr(server, 'history')

        # Only allowed attributes
        assert hasattr(server, 'server')
        assert hasattr(server, 'tools')

    def test_logging_configured(self):
        """Test that logging is properly configured."""
        logger = logging.getLogger('phase_iii.mcp_server.server')

        # Logger should exist
        assert logger is not None

        # Should have handlers (from basicConfig)
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) > 0


class TestToolHandlers:
    """Test MCP tool handler integration."""

    def test_tool_handlers_are_async(self):
        """Test that all tool handlers are async functions."""
        from phase_iii.mcp_server.tools.todo_tools import (
            create_todo_tool,
            list_todos_tool,
            update_todo_tool,
            delete_todo_tool,
            get_todo_tool
        )

        import inspect

        assert inspect.iscoroutinefunction(create_todo_tool)
        assert inspect.iscoroutinefunction(list_todos_tool)
        assert inspect.iscoroutinefunction(update_todo_tool)
        assert inspect.iscoroutinefunction(delete_todo_tool)
        assert inspect.iscoroutinefunction(get_todo_tool)

    @pytest.mark.asyncio
    async def test_create_todo_validation(self):
        """Test create_todo input validation."""
        from phase_iii.mcp_server.tools.todo_tools import create_todo_tool

        # Missing user_id
        result = await create_todo_tool({"title": "Test"})
        assert result["success"] is False
        assert "user_id" in result["error"]

        # Empty title
        result = await create_todo_tool({"user_id": 1, "title": ""})
        assert result["success"] is False
        assert "empty" in result["error"].lower()

        # Invalid user_id type
        result = await create_todo_tool({"user_id": "invalid", "title": "Test"})
        assert result["success"] is False

    @pytest.mark.asyncio
    async def test_list_todos_validation(self):
        """Test list_todos input validation."""
        from phase_iii.mcp_server.tools.todo_tools import list_todos_tool

        # Missing user_id
        result = await list_todos_tool({})
        assert result["success"] is False
        assert "user_id" in result["error"]

        # Invalid user_id type
        result = await list_todos_tool({"user_id": "invalid"})
        assert result["success"] is False

    @pytest.mark.asyncio
    async def test_update_todo_validation(self):
        """Test update_todo input validation."""
        from phase_iii.mcp_server.tools.todo_tools import update_todo_tool

        # Missing required fields
        result = await update_todo_tool({"user_id": 1})
        assert result["success"] is False

        result = await update_todo_tool({"todo_id": 1})
        assert result["success"] is False

        # No fields to update
        result = await update_todo_tool({"user_id": 1, "todo_id": 1})
        assert result["success"] is False
        assert "No fields" in result["error"]

    @pytest.mark.asyncio
    async def test_delete_todo_validation(self):
        """Test delete_todo input validation."""
        from phase_iii.mcp_server.tools.todo_tools import delete_todo_tool

        # Missing user_id
        result = await delete_todo_tool({"todo_id": 1})
        assert result["success"] is False

        # Missing todo_id
        result = await delete_todo_tool({"user_id": 1})
        assert result["success"] is False

    @pytest.mark.asyncio
    async def test_get_todo_validation(self):
        """Test get_todo input validation."""
        from phase_iii.mcp_server.tools.todo_tools import get_todo_tool

        # Missing user_id
        result = await get_todo_tool({"todo_id": 1})
        assert result["success"] is False

        # Missing todo_id
        result = await get_todo_tool({"user_id": 1})
        assert result["success"] is False


def run_unit_tests():
    """Run all unit tests and report results."""
    print("=" * 60)
    print("MCP SERVER UNIT TESTS")
    print("=" * 60)
    print()

    # Run pytest
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short"
    ])

    return exit_code == 0


if __name__ == "__main__":
    success = run_unit_tests()
    exit(0 if success else 1)
