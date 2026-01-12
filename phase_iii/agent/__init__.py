"""
AI Agent Package for Phase III

This package contains the AI agent implementation for conversational
todo management using Claude (Anthropic).

Main components:
    - TodoAgent: Main agent class
    - AgentConfig: Configuration management
    - System prompts: Agent behavior guidance
    - Tool definitions: MCP tool schemas
"""

from .agent import TodoAgent, create_agent
from .config.agent_config import AgentConfig, get_agent_config
from .config.tool_definitions import get_mcp_tool_definitions, get_tool_by_name
from .prompts.system_prompt import get_system_prompt

__all__ = [
    'TodoAgent',
    'create_agent',
    'AgentConfig',
    'get_agent_config',
    'get_mcp_tool_definitions',
    'get_tool_by_name',
    'get_system_prompt'
]