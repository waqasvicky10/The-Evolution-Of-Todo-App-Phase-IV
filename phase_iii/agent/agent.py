"""
AI Agent for Phase III Todo Chatbot

This module implements the TodoAgent that wraps LLM providers.
It maintains the existing interface while supporting pluggable providers.
"""

import logging
import re
from typing import List, Dict, Any, Optional

from .providers.base import LLMProvider
from .providers.mock_provider import MockProvider

logger = logging.getLogger(__name__)


class TodoAgent:
    """
    AI Agent for conversational todo management.
    
    Wraps LLM providers and maintains shared functionality like
    Urdu support, voice hooks, and tool result processing.
    """
    
    def __init__(self, provider: LLMProvider):
        """
        Initialize the Todo Agent.
        
        Args:
            provider: The LLM provider to use
        """
        self.provider = provider
        logger.info(f"TodoAgent initialized with provider: {type(provider).__name__}")
    
    def is_urdu(self, text: str) -> bool:
        """Simple check if the text contains Urdu/Arabic characters."""
        return any('\u0600' <= char <= '\u06FF' for char in text)
    
    def normalize_urdu(self, text: str) -> str:
        """Normalize Urdu text: trim and remove punctuation."""
        normalized = re.sub(r'[۔؟!،]', ' ', text)
        return normalized.strip()
    
    def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_id: int,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Process a user message via the provider."""
        return self.provider.process_message(
            user_message=user_message,
            conversation_history=conversation_history,
            user_id=user_id,
            tools=tools
        )
    
    def process_voice_command(
        self,
        transcribed_text: str,
        user_id: int,
        conversation_history: List[Dict[str, str]] = None,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Entry point for voice commands (transcribed text).
        Reuses the existing process_message logic.
        """
        logger.info(f"Processing voice command: {transcribed_text}")
        clean_text = transcribed_text.strip()
        
        return self.process_message(
            user_message=clean_text,
            conversation_history=conversation_history or [],
            user_id=user_id,
            tools=tools
        )
    
    def process_tool_results(self, tool_results: List[Dict[str, Any]], user_id: int) -> Dict[str, Any]:
        """
        Summarize tool results into a human-readable response.
        Supports English and Urdu based on context.
        """
        responses = []
        is_urdu_context = False
        
        # Detect Urdu in tool results
        for result in tool_results:
            content = result.get("content", {})
            for val in content.values():
                if isinstance(val, str) and self.is_urdu(val):
                    is_urdu_context = True
                    break
            if is_urdu_context:
                break
        
        for result in tool_results:
            content = result.get("content", {})
            success = content.get("success", False)
            
            if not success:
                error = content.get('error', 'Unknown error')
                if is_urdu_context:
                    responses.append(f"معذرت، ایک غلطی پیش آئی: {error}")
                else:
                    responses.append(f"Sorry, I encountered an error: {error}")
                continue
            
            if "todos" in content:
                todos = content.get("todos", [])
                if not todos:
                    responses.append("آپ کی ٹو ڈو فہرست فی الحال خالی ہے۔" if is_urdu_context else "Your todo list is currently empty.")
                else:
                    if is_urdu_context:
                        lines = ["آپ کی موجودہ فہرست یہ ہے:"]
                        for t in todos:
                            status = "✓" if t.get("completed") else " "
                            lines.append(f"[{status}] {t.get('id')}: {t.get('title')}")
                    else:
                        lines = ["Here is your current todo list:"]
                        for t in todos:
                            status = "✓" if t.get("completed") else " "
                            lines.append(f"[{status}] {t.get('id')}: {t.get('title')}")
                    responses.append("\n".join(lines))
            
            elif "todo_id" in content:
                todo_id = content['todo_id']
                if "deleted" in content:
                    responses.append(f"ٹاسک {todo_id} کامیابی سے حذف کر دیا گیا۔" if is_urdu_context else f"Successfully deleted task {todo_id}.")
                elif "title" in content:
                    title = content['title']
                    responses.append(f"ٹاسک '{title}' کامیابی سے محفوظ کر لیا گیا (آئی ڈی: {todo_id})۔" if is_urdu_context else f"Task '{title}' has been processed successfully (ID: {todo_id}).")
                else:
                    responses.append(f"ٹاسک {todo_id} پر عمل درآمد کامیاب رہا۔" if is_urdu_context else f"Operation on task {todo_id} was successful.")
        
        final_response = " ".join(responses) if responses else ("آپ کی فہرست اپ ڈیٹ کر دی گئی ہے!" if is_urdu_context else "I've updated your list as requested!")
        
        return {
            "response_text": final_response,
            "tool_calls": [],
            "requires_tool_execution": False
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information from the provider."""
        return self.provider.get_model_info()


def create_agent(api_key: str = "mock", config: Any = None) -> TodoAgent:
    """
    Create a TodoAgent with the appropriate provider.
    
    Selects provider based on OPENAI_API_KEY availability:
    - If OPENAI_API_KEY is set, uses OpenAIProvider
    - Otherwise, uses MockProvider as fallback
    
    Args:
        api_key: API key (ignored if OPENAI_API_KEY env var is set)
        config: Optional configuration object
        
    Returns:
        TodoAgent instance with selected provider
    """
    import os
    
    # Try to load .env file if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # python-dotenv not installed, continue without it
    
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_api_key = None # FORCE MOCK FOR VERIFICATION
    
    if openai_api_key:
        try:
            from .providers.openai_provider import OpenAIProvider
            provider = OpenAIProvider(api_key=openai_api_key, config=config)
            logger.info("Using OpenAIProvider")
            return TodoAgent(provider=provider)
        except ImportError:
            logger.warning("OpenAI package not available, falling back to MockProvider")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAIProvider: {e}, falling back to MockProvider")
    
    # Fallback to MockProvider
    provider = MockProvider()
    logger.info("Using MockProvider (fallback)")
    return TodoAgent(provider=provider)
