"""
Mock AI Agent for Phase III Todo Chatbot

This module implements a keyword-based mock agent that mimics the behavior
of an AI agent without requiring external API calls. It supports basic
todo management commands via simple string matching and regex.

Architecture:
- Stateless: No conversation state stored in agent.
- Tool-based: Generates tool call objects for the API layer to execute.
- No External Dependencies: No OpenAI or Anthropic SDKs required.
"""

import logging
import re
import json
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class TodoAgent:
    """
    Mock AI Agent for conversational todo management.
    
    Uses keyword matching to identify user intent and generate tool calls.
    """

    def __init__(self, api_key: str = "mock_key", config: Any = None):
        """
        Initialize the Mock Todo Agent.
        
        Args:
            api_key: Not used, kept for signature compatibility.
            config: Not used, kept for signature compatibility.
        """
        self.api_key = api_key
        logger.info("Mock TodoAgent initialized (No External APIs)")

    def is_urdu(self, text: str) -> bool:
        """Simple check if the text contains Urdu/Arabic characters."""
        return any('\u0600' <= char <= '\u06FF' for char in text)

    def normalize_urdu(self, text: str) -> str:
        """Normalize Urdu text: trim and remove punctuation."""
        # Remove Urdu/Arabic punctuation: ۔ ؟ ! ،
        normalized = re.sub(r'[۔؟!،]', ' ', text)
        return normalized.strip()

    def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_id: int,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return a mock agent response with tool calls.
        Supports English and Urdu.
        """
        is_urdu_msg = self.is_urdu(user_message)
        msg = self.normalize_urdu(user_message.lower()) if is_urdu_msg else user_message.lower().strip()
        logger.info(f"Mock processing message: {msg} (Urdu: {is_urdu_msg})")

        tool_calls = []
        response_text = ""

        # Ordinal Mapping for Urdu
        urdu_ordinals = {
            "پہلا": 1, "پہلے": 1,
            "دوسرا": 2, "دوسرے": 2,
            "تیسرا": 3, "تیسرے": 3,
            "چوتھا": 4, "چوتھے": 4,
            "پانچواں": 5, "پانچویں": 5
        }

        # Defining Rule-Based Parsing
        # Each rule: (intent, regex, response_generator)
        
        if is_urdu_msg:
            rules = [
                # List: "فہرست دکھائیں", "میری ٹاسک دکھاؤ", "کاموں کی فہرست دکھاؤ", "کیا ہیں میرے کام"
                ("list", r"(فہرست|لسٹ|دکھا|دیکھ|بتا|کیا ہے|کیا ہیں|میرے کام|ٹاسک|لسٹ)", 
                 lambda m: ("آپ کی ٹو ڈو فہرست حاصل کی جا رہی ہے...", [])),
                
                # Add: "دودھ خریدنا شامل کریں", "شامل کریں کتاب پڑھنا", "دودھ خریدنا شامل کرو", "ڈالو", "اضافہ کرو"
                ("add", r"(.*?)\s*(شامل کریں|شامل کرو|لکھیں|ایڈ کریں|ڈالیں|ڈالو|اضافہ کرو|کریں|بنائیں)", 
                 lambda m: (f"جی بالکل! میں '{m.group(1).strip()}' کو آپ کی فہرست میں شامل کر رہا ہوں۔", 
                            [{"name": "create_todo", "input": {"user_id": user_id, "title": m.group(1).strip()}}])),
                
                # Complete: "ٹاسک 5 مکمل کریں", "5 نمبر کام ہو گیا", "پہلا کام مکمل کرو"
                ("complete", r"(ٹاسک|کام|نمبر)?\s*(\d+|پہلا|دوسرا|تیسرا|چوتھا|پانچواں)\s*(ٹاسک|کام|نمبر)?\s*(مکمل|ختم|ہو گیا|ڈن|کریں|کردیں|کرو)", 
                 lambda m: (f"ٹاسک {m.group(2)} کو مکمل نشان زد کیا جا رہا ہے۔", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": urdu_ordinals.get(m.group(2), int(m.group(2)) if m.group(2).isdigit() else 1), "completed": True}}])),
                
                # Delete: "ٹاسک 10 حذف کریں", "10 کو مٹائیں", "دوسرا کام حذف کرو", "ڈیلیٹ کرو"
                ("delete", r"(ٹاسک|کام|نمبر)?\s*(\d+|پہلا|دوسرا|تیسرا|چوتھا|پانچواں)\s*(ٹاسک|کام|نمبر)?\s*(حذف|نکال|مٹائیں|ختم کریں|کرو|کریں|ڈیلیٹ)", 
                 lambda m: (f"میں آپ کے لیے ٹاسک {m.group(2)} حذف کر رہا ہوں۔", 
                            [{"name": "delete_todo", "input": {"user_id": user_id, "todo_id": urdu_ordinals.get(m.group(2), int(m.group(2)) if m.group(2).isdigit() else 1)}}])),
                
                # Update: "ٹاسک 1 کا نام بدل کر 'کتاب' کر دیں", "اپڈیٹ کرو"
                ("update", r"(ٹاسک|کام|نمبر)?\s*(\d+|پہلا|دوسرا|تیسرا|چوتھا|پانچواں)\s*(ٹاسک|کام|نمبر)?\s*(کا نام بدل کر|کو بدل کر|کو|بدلو|اپڈیٹ کرو|اپڈیٹ)\s*['\"]?(.*?)['\"]?\s*(کر دیں|تبدیل کریں|بنا دیں|کرو|کریں)", 
                 lambda m: (f"ٹاسک {m.group(2)} کو '{m.group(5).strip()}' میں تبدیل کیا جا رہا ہے۔", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": urdu_ordinals.get(m.group(2), int(m.group(2)) if m.group(2).isdigit() else 1), "title": m.group(5).strip()}}])),
            ]
        else:
            rules = [
                # List: "Show my list", "Fetch tasks"
                ("list", r"(show|list|get|fetch|what are|display).*(task|todo|list|items)", 
                 lambda m: ("Fetching your todo list...", [])),
                
                # Add: "Add buy milk", "Remember to call mom"
                ("add", r"(?:add|create|new task|remember to|remind me to)\s+(?:a task to|a task|to|task)?\s*(.+)", 
                 lambda m: (f"Sure! I'll add '{m.group(1).strip().capitalize()}' to your list.", 
                            [{"name": "create_todo", "input": {"user_id": user_id, "title": m.group(1).strip().capitalize()}}])),
                
                # Complete (Reverse): "Task 3 done", "5 is completed"
                ("complete", r"(?:task|todo|id|number)?\s*(\d+)\s*(?:is\s+)?(?:done|complete|completed|finished|ready)", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),

                # Complete: "Mark 5 as done", "Complete task 3", "Completed task 3", "Task 3 done"
                ("complete", r"(?:mark|set|mark task|complete|completed|finish|finished|done)\s+(?:task|todo|id)?\s*(\d+)\s*(?:as\s+)?(?:done|complete|completed|finished|ready)?", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                
                # Delete: "Delete task 10", "Remove 5", "Deleted task 5"
                ("delete", r"(?:delete|deleted|remove|removed|clear|erase|drop)\s+(?:task|todo|id)?\s*(\d+)", 
                 lambda m: (f"I'm deleting task {m.group(1)} for you.", 
                            [{"name": "delete_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1))}}])),
                
                # Update: "Update 1 to 'Buy bread'", "Change task 2 to Study"
                ("update", r"(?:update|change|changed|edit|rename)\s+(?:task|todo|id)?\s*(\d+)\s+(?:to|with)\s+['\"]?(.*?)['\"]?$", 
                 lambda m: (f"Updating task {m.group(1)} to '{m.group(2).strip()}'.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "title": m.group(2).strip()}}])),
            ]

        # Apply Rules
        matched = False
        for intent, pattern, generator in rules:
            match = re.search(pattern, msg, re.IGNORECASE) if not is_urdu_msg else re.search(pattern, user_message)
            if match:
                res_text, calls = generator(match)
                response_text = res_text
                tool_calls = calls
                # Handle special case for list which might not have tool calls in generator but we need them here
                if intent == "list":
                    tool_calls = [{
                        "tool_use_id": "mock_list_" + str(user_id),
                        "name": "list_todos",
                        "input": {"user_id": user_id}
                    }]
                elif tool_calls:
                    # Add mock tool_use_id
                    for i, call in enumerate(tool_calls):
                        call["tool_use_id"] = f"mock_{intent}_{i}_{user_id}"
                
                matched = True
                break

        if not matched:
            if is_urdu_msg:
                response_text = "معذرت، میں سمجھ نہیں سکا۔ میں کام شامل کرنے، فہرست دیکھنے، اپ ڈیٹ کرنے یا حذف کرنے میں آپ کی مدد کر سکتا ہوں۔"
            else:
                response_text = "I'm sorry, I didn't quite catch that. I can help you add, list, update, or delete tasks."

        return {
            "response_text": response_text,
            "tool_calls": tool_calls,
            "requires_tool_execution": len(tool_calls) > 0,
            "stop_reason": "end_turn",
            "language": "ur" if is_urdu_msg else "en"
        }

    def process_voice_command(
        self,
        transcribed_text: str,
        user_id: int,
        conversation_history: List[Dict[str, str]] = None,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Entry point for voice commands (transcribed text).
        Reuses the existing process_message logic for deterministic parsing.
        """
        logger.info(f"Processing voice command: {transcribed_text}")
        # Standardize transcribed text (might be needed if STT gives weird casing/spacing)
        clean_text = transcribed_text.strip()
        
        # Route through the existing robust parser
        return self.process_message(
            user_message=clean_text,
            conversation_history=conversation_history or [],
            user_id=user_id,
            tools=tools
        )

    def process_tool_results(self, tool_results: List[Dict[str, Any]], user_id: int) -> Dict[str, Any]:
        """
        Summarize tool results into a human-readable response.
        Supports English and Urdu based on context (inferred from first result or default).
        """
        responses = []
        # Detection logic: if any result content has Urdu, we might want to respond in Urdu
        # Or better: check the context if possible. Since we're stateless, let's peek at the tool_results 
        # for any clues or default to English. However, we can also store language in tool_results if needed.
        # For now, let's use a simple Urdu detection on any existing text in tool results if any, 
        # or stick to the logic that the caller should handle language preference.
        # IMPROVEMENT: Use the user's last message language if passed here.
        
        is_urdu_context = False
        for result in tool_results:
            content = result.get("content", {})
            for val in content.values():
                if isinstance(val, str) and self.is_urdu(val):
                    is_urdu_context = True
                    break
            if is_urdu_context: break

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

            if "todos" in content:  # list_todos result
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
        return {
            "model": "local-mock-v1",
            "provider": "local",
            "capabilities": ["english", "urdu", "voice-ready"]
        }

def create_agent(api_key: str = "mock", config: Any = None) -> TodoAgent:
    return TodoAgent(api_key=api_key, config=config)

def create_agent(api_key: str = "mock", config: Any = None) -> TodoAgent:
    return TodoAgent(api_key=api_key, config=config)
