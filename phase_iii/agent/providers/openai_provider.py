"""
OpenAI LLM Provider for Phase III

This provider implements OpenAI-based LLM calls using the OpenAI API.
"""

import json
import logging
import os
from typing import List, Dict, Any, Optional

try:
    from openai import OpenAI as OpenAIClient
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAIClient = None

from .base import LLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """
    OpenAI LLM provider using OpenAI API.
    
    This provider uses OpenAI's chat completions API with tool calling.
    """
    
    def __init__(self, api_key: str, config: Any = None):
        """
        Initialize the OpenAI Provider.
        
        Args:
            api_key: OpenAI API key
            config: Optional configuration object
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package is required for OpenAIProvider. Install with: pip install openai")
        
        self.api_key = api_key
        self.client = OpenAIClient(api_key=api_key)
        self.config = config
        
        # Default model
        self.model = getattr(config, 'model', 'gpt-4o-mini') if config else 'gpt-4o-mini'
        self.temperature = getattr(config, 'temperature', 0.7) if config else 0.7
        self.max_tokens = getattr(config, 'max_tokens', 4096) if config else 4096
        
        logger.info(f"OpenAIProvider initialized with model: {self.model}")
    
    def _convert_tools_to_openai_format(self, tools: Optional[List[Dict[str, Any]]]) -> Optional[List[Dict[str, Any]]]:
        """Convert MCP tool definitions to OpenAI function calling format."""
        if not tools:
            return None
        
        openai_tools = []
        for tool in tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("input_schema", {})
                }
            }
            openai_tools.append(openai_tool)
        
        return openai_tools
    
    def _convert_messages_to_openai_format(self, conversation_history: List[Dict[str, str]], user_message: str) -> List[Dict[str, Any]]:
        """Convert conversation history to OpenAI message format."""
        messages = []
        
        # Add conversation history
        for msg in conversation_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            # Map assistant/user roles
            if role == "assistant":
                messages.append({"role": "assistant", "content": content})
            else:
                messages.append({"role": "user", "content": content})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_id: int,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Process a user message using OpenAI API."""
        try:
            # Convert tools to OpenAI format
            openai_tools = self._convert_tools_to_openai_format(tools)
            
            # Convert messages to OpenAI format
            messages = self._convert_messages_to_openai_format(conversation_history, user_message)
            
            # Call OpenAI API
            logger.info(f"Calling OpenAI API with model: {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=openai_tools,
                tool_choice="auto",
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extract response
            choice = response.choices[0]
            message = choice.message
            
            # Extract tool calls
            tool_calls = []
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    try:
                        arguments = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {tool_call.function.arguments}")
                        arguments = {}
                    
                    tool_calls.append({
                        "tool_use_id": tool_call.id,
                        "name": tool_call.function.name,
                        "input": arguments
                    })
            
            # Determine language (simple check)
            response_text = message.content or ""
            language = "ur" if any('\u0600' <= char <= '\u06FF' for char in response_text + user_message) else "en"
            
            return {
                "response_text": response_text,
                "tool_calls": tool_calls,
                "requires_tool_execution": len(tool_calls) > 0,
                "stop_reason": choice.finish_reason or "end_turn",
                "language": language
            }
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}", exc_info=True)
            # Fallback to a simple error response
            return {
                "response_text": "I'm sorry, I encountered an error processing your request. Please try again.",
                "tool_calls": [],
                "requires_tool_execution": False,
                "stop_reason": "error",
                "language": "en"
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get OpenAI provider info."""
        return {
            "model": self.model,
            "provider": "openai",
            "capabilities": ["english", "urdu", "voice-ready"]
        }
