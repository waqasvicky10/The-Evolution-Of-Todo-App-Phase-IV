"""
Mock LLM Provider for Phase III

This provider implements keyword-based mock logic without external APIs.
Extracted from the original TodoAgent implementation.
"""

import logging
import re
from typing import List, Dict, Any, Optional

from .base import LLMProvider

logger = logging.getLogger(__name__)


class MockProvider(LLMProvider):
    """
    Mock LLM provider using keyword-based intent recognition.
    
    This is the fallback provider when no API key is available.
    """
    
    def __init__(self):
        """Initialize the Mock Provider."""
        logger.info("MockProvider initialized (No External APIs)")
    
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
        """Process a user message using keyword matching."""
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
        
        if is_urdu_msg:
            rules = [
                ("list", r"(فہرست|لسٹ|دکھا|دیکھ|بتا|کیا ہے|کیا ہیں|میرے کام|ٹاسک|لسٹ)", 
                 lambda m: ("آپ کی ٹو ڈو فہرست حاصل کی جا رہی ہے...", [])),
                ("add", r"(.*?)\s*(شامل کریں|شامل کرو|لکھیں|ایڈ کریں|ڈالیں|ڈالو|اضافہ کرو|کریں|بنائیں)", 
                 lambda m: (f"جی بالکل! میں '{m.group(1).strip()}' کو آپ کی فہرست میں شامل کر رہا ہوں۔", 
                            [{"name": "create_todo", "input": {"user_id": user_id, "title": m.group(1).strip()}}])),
                ("complete", r"(ٹاسک|کام|نمبر)?\s*(\d+|پہلا|دوسرا|تیسرا|چوتھا|پانچواں)\s*(ٹاسک|کام|نمبر)?\s*(مکمل|ختم|ہو گیا|ڈن|کریں|کردیں|کرو)", 
                 lambda m: (f"ٹاسک {m.group(2)} کو مکمل نشان زد کیا جا رہا ہے۔", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": urdu_ordinals.get(m.group(2), int(m.group(2)) if m.group(2).isdigit() else 1), "completed": True}}])),
                ("delete", r"(ٹاسک|کام|نمبر)?\s*(\d+|پہلا|دوسرا|تیسرا|چوتھا|پانچواں)\s*(ٹاسک|کام|نمبر)?\s*(حذف|نکال|مٹائیں|ختم کریں|کرو|کریں|ڈیلیٹ)", 
                 lambda m: (f"میں آپ کے لیے ٹاسک {m.group(2)} حذف کر رہا ہوں۔", 
                            [{"name": "delete_todo", "input": {"user_id": user_id, "todo_id": urdu_ordinals.get(m.group(2), int(m.group(2)) if m.group(2).isdigit() else 1)}}])),
                ("update", r"(ٹاسک|کام|نمبر)?\s*(\d+|پہلا|دوسرا|تیسرا|چوتھا|پانچواں)\s*(ٹاسک|کام|نمبر)?\s*(کا نام بدل کر|کو بدل کر|کو|بدلو|اپڈیٹ کرو|اپڈیٹ)\s*['\"]?(.*?)['\"]?\s*(کر دیں|تبدیل کریں|بنا دیں|کرو|کریں)", 
                 lambda m: (f"ٹاسک {m.group(2)} کو '{m.group(5).strip()}' میں تبدیل کیا جا رہا ہے۔", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": urdu_ordinals.get(m.group(2), int(m.group(2)) if m.group(2).isdigit() else 1), "title": m.group(5).strip()}}])),
            ]
        else:
            rules = [
                ("list", r"(show|list|get|fetch|what are|display).*(task|todo|list|items)", 
                 lambda m: ("Fetching your todo list...", [])),
                ("add", r"(?:add|create|new task|remember to|remind me to)\s+(?:a task to|a task|to|task)?\s*(.+)", 
                 lambda m: (f"Sure! I'll add '{m.group(1).strip().capitalize()}' to your list.", 
                            [{"name": "create_todo", "input": {"user_id": user_id, "title": m.group(1).strip().capitalize()}}])),
                # Handle "ID 24 marked as completed task" format (most specific - must come first)
                ("complete", r"id\s+(\d+)\s+marked\s+as\s+(?:completed|complete|done|finished)\s+task", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                # Handle "ID 24 marked as completed" format (without "task" at end)
                ("complete", r"id\s+(\d+)\s+marked\s+as\s+(?:completed|complete|done|finished)", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                # Handle "ID 6 task completed" format
                ("complete", r"id\s+(\d+)\s+task\s+(?:is\s+)?(?:done|complete|completed|finished|ready)", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                # Handle "ID 24 marked as completed" format
                ("complete", r"id\s+(\d+)\s+marked\s+as\s+(?:completed|complete|done|finished)", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                # Handle "task 6 completed" format
                ("complete", r"task\s+(\d+)\s+(?:is\s+)?(?:done|complete|completed|finished|ready)", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                # Handle "task 6 done" format
                ("complete", r"task\s+(\d+)\s+done", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                # Handle "complete task 6" format
                ("complete", r"(?:complete|mark|set|finish)\s+task\s+(\d+)", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                # Handle "ID 6 completed" format
                ("complete", r"id\s+(\d+)\s+(?:is\s+)?(?:done|complete|completed|finished|ready)", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                # Handle "6 completed" format (standalone number)
                ("complete", r"^(\d+)\s+(?:is\s+)?(?:done|complete|completed|finished|ready)$", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                # Handle "(mark|set|mark task|complete|completed|finish|finished|done)\s+(?:task|todo|id)?\s*(\d+)\s*(?:as\s+)?(?:done|complete|completed|finished|ready)?" format
                ("complete", r"(?:mark|set|mark task|complete|completed|finish|finished|done)\s+(?:task|todo|id)?\s*(\d+)\s*(?:as\s+)?(?:done|complete|completed|finished|ready)?", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                # Handle "(task|todo|id|number)?\s*(\d+)\s*(?:is\s+)?(?:done|complete|completed|finished|ready)" format (most general)
                ("complete", r"(?:task|todo|id|number)?\s*(\d+)\s*(?:is\s+)?(?:done|complete|completed|finished|ready)", 
                 lambda m: (f"Marking task {m.group(1)} as complete.", 
                            [{"name": "update_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1)), "completed": True}}])),
                # Handle "ID 24 delete tasks" format (most specific - must come first)
                ("delete", r"id\s+(\d+)\s+(?:delete|deleted|remove|removed|clear|erase|drop)\s+(?:task|tasks|todo|todos)", 
                 lambda m: (f"I'm deleting task {m.group(1)} for you.", 
                            [{"name": "delete_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1))}}])),
                # Handle "ID 24 delete" format
                ("delete", r"id\s+(\d+)\s+(?:delete|deleted|remove|removed|clear|erase|drop)", 
                 lambda m: (f"I'm deleting task {m.group(1)} for you.", 
                            [{"name": "delete_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1))}}])),
                # Handle "delete task 24" format
                ("delete", r"(?:delete|deleted|remove|removed|clear|erase|drop)\s+(?:task|todo|id)?\s*(\d+)", 
                 lambda m: (f"I'm deleting task {m.group(1)} for you.", 
                            [{"name": "delete_todo", "input": {"user_id": user_id, "todo_id": int(m.group(1))}}])),
                ("update", r"(?:update|change|changed|edit|rename)\s+(?:task|todo|id)?\s*(\d+)\s+(?:to|with)\s+['\"]?(.*?)['\"]?$", 
                 lambda m: (f"Updating task {m.group(1)} to '{m.group(2).strip()}'." , 
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
                if intent == "list":
                    tool_calls = [{
                        "tool_use_id": "mock_list_" + str(user_id),
                        "name": "list_todos",
                        "input": {"user_id": user_id}
                    }]
                elif tool_calls:
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
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get mock provider info."""
        return {
            "model": "local-mock-v1",
            "provider": "local",
            "capabilities": ["english", "urdu", "voice-ready"]
        }
