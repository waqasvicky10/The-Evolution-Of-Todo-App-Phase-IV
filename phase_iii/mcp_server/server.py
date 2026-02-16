"""
MCP Server for Phase III Todo Application

This module implements a Model Context Protocol (MCP) server that exposes
todo management tools to AI agents using the official MCP SDK.

The server is stateless and delegates all data operations to the Phase II
Streamlit backend through the shared SQLite database.

Server Features:
- Stateless operation (no conversation state)
- Clean startup/shutdown lifecycle
- Health check endpoint
- Structured logging
- Tool registration and invocation handling

References:
    - PHASE_III_SPECIFICATION.md: MCP Server Requirements
    - PHASE_III_PLAN.md: Task 2 - MCP Server Implementation
    - Official MCP SDK: https://github.com/modelcontextprotocol/python-sdk
"""

import logging
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Import tool implementations
from phase_iii.mcp_server.tools.todo_tools import (
    create_todo_tool,
    add_task_tool,
    get_user_context_tool,
    list_todos_tool,
    list_tasks_tool,
    search_tasks_tool,
    update_todo_tool,
    update_task_tool,
    complete_task_tool,
    delete_todo_tool,
    remove_task_tool,
    get_todo_tool
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TodoMCPServer:
    """
    MCP Server for Todo Management Tools.

    This server exposes todo CRUD operations as MCP tools that can be
    invoked by AI agents through the Model Context Protocol.

    Architecture:
        - Stateless: No conversation history or user session tracking
        - Delegates: All data operations go to Phase II backend
        - Clean lifecycle: Proper startup/shutdown handling

    Attributes:
        server: MCP Server instance
        tools: Registry of available tools
    """

    def __init__(self):
        """Initialize the MCP server."""
        self.server = Server("todo-mcp-server")
        self.tools: Dict[str, Any] = {}
        logger.info("TodoMCPServer initialized")

    def register_tools(self) -> None:
        """
        Register all available tools with the MCP server.

        Tools registered:
            - create_todo: Create a new todo item
            - add_task: Create a new todo item (alias)
            - get_user_context: Retrieve user identity and metadata
            - list_todos: List user's todo items
            - list_tasks: List user's todo items (alias)
            - search_tasks: Search and filter tasks (alias)
            - update_todo: Update an existing todo
            - update_task: Update an existing todo (alias)
            - complete_task: Mark a todo as completed (alias)
            - delete_todo: Delete a todo item
            - remove_task: Delete a todo item (alias)
            - get_todo: Get a specific todo by ID
        """
        # Register tool handlers
        self.tools = {
            "get_user_context": get_user_context_tool,
            "create_todo": create_todo_tool,
            "add_task": add_task_tool,
            "list_todos": list_todos_tool,
            "list_tasks": list_tasks_tool,
            "search_tasks": search_tasks_tool,
            "update_todo": update_todo_tool,
            "update_task": update_task_tool,
            "complete_task": complete_task_tool,
            "delete_todo": delete_todo_tool,
            "remove_task": remove_task_tool,
            "get_todo": get_todo_tool
        }

        # Register list_tools handler
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """Return list of available tools."""
            return [
            Tool(
                name="get_user_context",
                description="Retrieve user profile and identity context (email, name, registration date)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "ID of the authenticated user"
                        }
                    },
                    "required": ["user_id"]
                }
            ),
            Tool(
                name="create_todo",
                    description="Create a new todo item for a user",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "ID of the authenticated user"
                            },
                            "title": {
                                "type": "string",
                                "description": "Todo item title"
                            },
                            "description": {
                                "type": "string",
                                "description": "Additional description or notes (optional)"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "Initial completion status (default: false)"
                            }
                        },
                        "required": ["user_id", "title"]
                    }
                ),
                Tool(
                    name="add_task",
                    description="Create a new todo item for a user",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "ID of the authenticated user"
                            },
                            "title": {
                                "type": "string",
                                "description": "Task title"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional task description/details"
                            }
                        },
                        "required": ["user_id", "title"]
                    }
                ),
                Tool(
                    name="list_todos",
                    description="List all todo items for a user",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "ID of the authenticated user"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "Filter by completion status (optional)"
                            },
                            "status": {
                                "type": "string",
                                "description": "Filter by status: 'all', 'pending', or 'completed' (optional, default: 'all')"
                            },
                            "priority": {
                                "type": "string",
                                "description": "Filter by priority: 'high', 'medium', or 'low' (optional)"
                            },
                            "category": {
                                "type": "string",
                                "description": "Filter by category (optional)"
                            },
                            "keyword": {
                                "type": "string",
                                "description": "Search keyword in description (optional)"
                            }
                        },
                        "required": ["user_id"]
                    }
                ),
                Tool(
                    name="list_tasks",
                    description="List all todo items for a user with optional search/filters",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "ID of the authenticated user"
                            },
                            "status": {
                                "type": "string",
                                "description": "Filter by status: 'all', 'pending', or 'completed' (optional, default: 'all')"
                            },
                            "priority": {
                                "type": "string",
                                "description": "Filter by priority: 'high', 'medium', or 'low' (optional)"
                            },
                            "category": {
                                "type": "string",
                                "description": "Filter by category (optional)"
                            },
                            "keyword": {
                                "type": "string",
                                "description": "Search keyword in description (optional)"
                            }
                        },
                        "required": ["user_id"]
                    }
                ),
                Tool(
                    name="search_tasks",
                    description="Search and filter tasks by keywords, priority, and category",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "ID of the authenticated user"
                            },
                            "status": {
                                "type": "string",
                                "description": "Filter by status: 'all', 'pending', or 'completed' (optional, default: 'all')"
                            },
                            "priority": {
                                "type": "string",
                                "description": "Filter by priority: 'high', 'medium', or 'low' (optional)"
                            },
                            "category": {
                                "type": "string",
                                "description": "Filter by category (optional)"
                            },
                            "keyword": {
                                "type": "string",
                                "description": "Search keyword in description (optional)"
                            }
                        },
                        "required": ["user_id"]
                    }
                ),
                Tool(
                    name="update_todo",
                    description="Update an existing todo item",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "ID of the authenticated user"
                            },
                            "todo_id": {
                                "type": "integer",
                                "description": "ID of the todo item to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title (optional)"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "New completion status (optional)"
                            }
                        },
                        "required": ["user_id", "todo_id"]
                    }
                ),
                        "required": ["user_id", "todo_id"]
                    }
                ),
                        "required": ["user_id", "todo_id"]
                    }
                ),
                Tool(
                    name="update_task",
                    description="Update a specific todo item's title or details",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "ID of the authenticated user"
                            },
                            "todo_id": {
                                "type": "integer",
                                "description": "ID of the todo item to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title for the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description for the task"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "Update completion status"
                            }
                        },
                        "required": ["user_id", "todo_id"]
                    }
                ),
                Tool(
                    name="complete_task",
                    description="Mark a specific todo item as completed",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "ID of the authenticated user"
                            },
                            "todo_id": {
                                "type": "integer",
                                "description": "ID of the todo item to mark as complete"
                            }
                        },
                        "required": ["user_id", "todo_id"]
                    }
                ),
                Tool(
                    name="delete_todo",
                    description="Delete a todo item",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "ID of the authenticated user"
                            },
                            "todo_id": {
                                "type": "integer",
                                "description": "ID of the todo item to delete"
                            }
                        },
                        "required": ["user_id", "todo_id"]
                    }
                ),
                        "required": ["user_id", "todo_id"]
                    }
                ),
                Tool(
                    name="remove_task",
                    description="Delete a todo item permanently",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "ID of the authenticated user"
                            },
                            "todo_id": {
                                "type": "integer",
                                "description": "ID of the todo item to delete"
                            }
                        },
                        "required": ["user_id", "todo_id"]
                    }
                ),
                Tool(
                    name="get_todo",
                    description="Get a specific todo item by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "ID of the authenticated user"
                            },
                            "todo_id": {
                                "type": "integer",
                                "description": "ID of the todo item to retrieve"
                            }
                        },
                        "required": ["user_id", "todo_id"]
                    }
                )
            ]

        # Register call_tool handler
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool invocation."""
            logger.info(f"Tool called: {name} with arguments: {arguments}")

            if name not in self.tools:
                error_msg = f"Unknown tool: {name}"
                logger.error(error_msg)
                return [TextContent(type="text", text=error_msg)]

            try:
                # Invoke the tool handler
                result = await self.tools[name](arguments)

                # Format result as TextContent
                import json
                result_text = json.dumps(result, indent=2)

                logger.info(f"Tool {name} completed successfully")
                return [TextContent(type="text", text=result_text)]

            except Exception as e:
                error_msg = f"Tool execution error: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return [TextContent(type="text", text=error_msg)]

        logger.info(f"Registered {len(self.tools)} tools")

    async def start(self) -> None:
        """
        Start the MCP server.

        Initializes tool registration and prepares the server for handling
        requests via stdio transport.
        """
        logger.info("Starting TodoMCPServer...")
        self.register_tools()
        logger.info("TodoMCPServer started successfully")

    async def stop(self) -> None:
        """
        Stop the MCP server gracefully.

        Performs cleanup operations before shutdown.
        """
        logger.info("Stopping TodoMCPServer...")
        # No persistent connections or state to clean up
        logger.info("TodoMCPServer stopped successfully")

    async def run(self) -> None:
        """
        Run the MCP server with stdio transport.

        This is the main entry point that starts the server and listens
        for MCP protocol messages on stdin/stdout.
        """
        await self.start()

        try:
            # Run server with stdio transport
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
        finally:
            await self.stop()


# Health check function
async def health_check() -> Dict[str, Any]:
    """
    Perform a health check on the MCP server.

    Returns:
        Dict with health status and server info

    Example:
        >>> status = await health_check()
        >>> print(status)
        {'status': 'healthy', 'server': 'todo-mcp-server', 'tools_count': 5}
    """
    return {
        "status": "healthy",
        "server": "todo-mcp-server",
        "version": "1.0.0",
        "tools_count": 5,
        "stateless": True
    }


# Main entry point
async def main():
    """Main entry point for running the MCP server."""
    server = TodoMCPServer()
    await server.run()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
