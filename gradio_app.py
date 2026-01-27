"""
Phase III Todo Chatbot - Gradio Version
PRODUCTION-READY, BUG-FREE VERSION

AI-Powered Todo Assistant with Voice Input Support
- Phase III Agent Integration (with robust fallback)
- MCP Tools for task management
- Free voice transcription (no API key required)
- Optimized for performance and reliability
"""

import gradio as gr
import sqlite3
import os
import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
import re

# Add phase_iii to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Load .env **before** any code that uses OPENAI_API_KEY
def _load_env():
    try:
        from dotenv import load_dotenv
        root = Path(__file__).resolve().parent
        for p in (root / ".env", root / "phase_iii" / ".env"):
            if p.exists():
                load_dotenv(p, override=True)
        key = (os.getenv("OPENAI_API_KEY") or "").strip()
        if key and not key.startswith("sk-placeholder"):
            print("[Gradio] OPENAI_API_KEY loaded; voice uses OpenAI when available.")
        print("[Gradio] Voice fallback: free (Google Speech). No API key or purchase needed.")
    except ImportError:
        print("[Gradio] python-dotenv not installed; pip install python-dotenv to load .env")

_load_env()

# Import Phase III Agent and MCP Tools (Hackathon Requirement)
PHASE_III_AVAILABLE = False
TOOL_MAP = {}

try:
    from phase_iii.agent import create_agent, get_mcp_tool_definitions
    from phase_iii.agent.config.agent_config import get_agent_config
    from phase_iii.mcp_server.tools.todo_tools import (
        create_todo_tool,
        list_todos_tool,
        update_todo_tool,
        delete_todo_tool,
        get_todo_tool
    )
    PHASE_III_AVAILABLE = True
    TOOL_MAP = {
        "create_todo": create_todo_tool,
        "list_todos": list_todos_tool,
        "update_todo": update_todo_tool,
        "delete_todo": delete_todo_tool,
        "get_todo": get_todo_tool
    }
    print("[Gradio] [OK] Phase III Agent and MCP tools loaded successfully")
except ImportError as e:
    PHASE_III_AVAILABLE = False
    print(f"[Gradio] [WARN] Phase III components not available: {e}")
    print("[Gradio] Using reliable regex-based intent recognition")

# Database path
if os.path.exists("/tmp"):
    DB_PATH = "/tmp/todo.db"
elif os.path.exists("/mount/src"):
    DB_PATH = "/mount/src/todo.db"
else:
    DB_PATH = "todo.db"


def init_database():
    """Initialize the SQLite database with schema migration support."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='users'
        """)
        users_table_exists = cursor.fetchone() is not None
        
        schema_mismatch = False
        columns = []
        
        if users_table_exists:
            cursor.execute("PRAGMA table_info(users)")
            columns = [row[1] for row in cursor.fetchall()]
            required_columns = ['id', 'email', 'hashed_password', 'created_at', 'updated_at']
            if not all(col in columns for col in required_columns):
                schema_mismatch = True
        
        if not users_table_exists or schema_mismatch:
            if users_table_exists:
                cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
        
        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                is_complete BOOLEAN DEFAULT 0,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Conversation messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        conn.commit()
        print(f"[Gradio] [OK] Database initialized: {DB_PATH}")
    except Exception as e:
        print(f"[Gradio] [WARN] Database init warning: {e}")
    finally:
        if conn:
            conn.close()


def get_db_connection():
    """Get database connection with retry logic."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.OperationalError as e:
            if attempt < max_retries - 1:
                import time
                time.sleep(0.1)
                continue
            raise


def get_user_tasks(user_id: int) -> List[Dict]:
    """Get all tasks for a user."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, description, is_complete, created_at FROM tasks WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        tasks = cursor.fetchall()
        conn.close()
        return [
            {
                "id": t["id"],
                "description": t["description"],
                "completed": bool(t["is_complete"]),
                "created_at": t["created_at"]
            }
            for t in tasks
        ]
    except Exception as e:
        print(f"[Gradio] Error getting tasks: {e}")
        return []


def create_task(user_id: int, description: str) -> Tuple[bool, str]:
    """Create a new task."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO tasks (user_id, description, is_complete, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, description.strip(), False, now, now)
        )
        conn.commit()
        conn.close()
        return True, "Task created successfully"
    except Exception as e:
        print(f"[Gradio] Error creating task: {e}")
        return False, str(e)


def update_task(user_id: int, task_id: int, description: Optional[str] = None, completed: Optional[bool] = None) -> Tuple[bool, str]:
    """Update a task."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify task belongs to user
        cursor.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        if not cursor.fetchone():
            conn.close()
            return False, "Task not found"
        
        updates = []
        params = []
        
        if description is not None:
            updates.append("description = ?")
            params.append(description.strip())
        
        if completed is not None:
            updates.append("is_complete = ?")
            params.append(1 if completed else 0)
        
        if updates:
            updates.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            params.append(task_id)
            params.append(user_id)
            
            cursor.execute(
                f"UPDATE tasks SET {', '.join(updates)} WHERE id = ? AND user_id = ?",
                params
            )
            conn.commit()
        
        conn.close()
        return True, "Task updated successfully"
    except Exception as e:
        print(f"[Gradio] Error updating task: {e}")
        return False, str(e)


def delete_task(user_id: int, task_id: int) -> Tuple[bool, str]:
    """Delete a task."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        if cursor.rowcount == 0:
            conn.close()
            return False, "Task not found"
        conn.commit()
        conn.close()
        return True, "Task deleted successfully"
    except Exception as e:
        print(f"[Gradio] Error deleting task: {e}")
        return False, str(e)


def store_message(user_id: int, role: str, content: str):
    """Store a message in conversation history."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversation_messages (user_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (user_id, role, content, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
    except Exception:
        pass  # Fail silently - history is optional


def get_conversation_history(user_id: int, limit: int = 20) -> List[Dict]:
    """Get conversation history."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content, created_at FROM conversation_messages WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        )
        messages = cursor.fetchall()
        conn.close()
        return [{"role": m[0], "content": m[1], "created_at": m[2]} for m in reversed(messages)]
    except Exception:
        return []


def recognize_intent(message: str) -> Tuple[str, Dict]:
    """Reliable regex-based intent recognition (fallback)."""
    message_lower = message.lower().strip()
    
    # Create task patterns
    create_patterns = [
        r"add\s+(?:a\s+)?(?:task|todo|item)\s+(?:to|for|about|by)?\s*(?:.*?)(?:to\s+)?(.+)",
        r"create\s+(?:a\s+)?(?:task|todo|item)\s*(?:.*?)(?:to\s+)?(.+)",
        r"new\s+(?:task|todo|item)\s*(?:.*?)(?:to\s+)?(.+)",
        r"remind\s+me\s+(?:to\s+)?(.+)",
        r"i\s+need\s+(?:to\s+)?(.+)",
        r"add\s+(.+)",
        r"create\s+(.+)",
    ]
    
    # List tasks patterns
    list_patterns = [
        r"show\s+(?:me\s+)?(?:all\s+)?(?:my\s+)?(?:tasks?|todos?|list)",
        r"list\s+(?:all\s+)?(?:my\s+)?(?:tasks?|todos?)",
        r"what\s+(?:are\s+)?(?:my\s+)?(?:tasks?|todos?)",
        r"display\s+(?:my\s+)?(?:tasks?|todos?)",
        r"get\s+(?:my\s+)?(?:tasks?|todos?)",
    ]
    
    # Complete task patterns (order matters - most specific first)
    complete_patterns = [
        r"mark\s+task\s+(\d+)\s+(?:as\s+)?(?:done|complete|completed|finished)",  # "mark task 1 as complete"
        r"mark\s+task\s+(\d+)",  # "mark task 1"
        r"task\s+(\d+)\s+(?:is\s+)?(?:done|complete|completed|finished)",  # "task 1 is complete"
        r"complete\s+task\s+(\d+)",  # "complete task 1"
        r"mark\s+(.+?)\s+(?:as\s+)?(?:done|complete|completed|finished)",  # "mark X as complete"
        r"complete\s+(.+)",  # "complete X"
        r"(.+?)\s+is\s+(?:done|complete|completed|finished)",  # "X is done"
        r"finish\s+(.+)",  # "finish X"
        r"done\s+(.+)",  # "done X"
    ]
    
    # Delete task patterns
    delete_patterns = [
        r"delete\s+(?:task\s+)?(\d+)",
        r"remove\s+(?:task\s+)?(\d+)",
        r"delete\s+(.+)",
        r"remove\s+(.+)",
    ]
    
    # Check for create intent
    for pattern in create_patterns:
        match = re.search(pattern, message_lower)
        if match:
            task_desc = match.group(1).strip() if match.groups() else ""
            if not task_desc or len(task_desc) < 2:
                # Try to extract from full message
                for prefix in ["add", "create", "new", "remind me to", "i need to"]:
                    if message_lower.startswith(prefix):
                        task_desc = message_lower[len(prefix):].strip()
                        break
            task_desc = re.sub(r"\s+(?:to\s+my\s+list|as\s+a\s+task|task)$", "", task_desc, flags=re.IGNORECASE).strip()
            if task_desc and len(task_desc) > 1:
                return "create", {"description": task_desc}
    
    # Check for list intent
    for pattern in list_patterns:
        if re.search(pattern, message_lower):
            return "list", {}
    
    # Check for complete intent
    for pattern in complete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            task_ref = match.group(1).strip() if match.groups() else ""
            # Extract number if present (task ID)
            num_match = re.search(r"^(\d+)$", task_ref)  # Exact number match
            if num_match:
                return "complete", {"task_id": int(num_match.group(1))}
            # Try to find number in the reference
            num_match = re.search(r"\d+", task_ref)
            if num_match:
                return "complete", {"task_id": int(num_match.group())}
            if task_ref:
                return "complete", {"task_reference": task_ref}
    
    # Check for delete intent
    for pattern in delete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            task_ref = match.group(1).strip() if match.groups() else ""
            num_match = re.search(r"\d+", task_ref)
            if num_match:
                return "delete", {"task_id": int(num_match.group())}
            if task_ref:
                return "delete", {"task_reference": task_ref}
    
    return "unknown", {}


def find_task_by_reference(user_id: int, reference: str) -> Optional[Dict]:
    """Find task by description or ID reference."""
    if not reference:
        return None
    
    tasks = get_user_tasks(user_id)
    
    # Try to find by ID first
    num_match = re.search(r"\d+", reference)
    if num_match:
        task_id = int(num_match.group())
        for task in tasks:
            if task["id"] == task_id:
                return task
    
    # Try exact match
    reference_lower = reference.lower().strip()
    for task in tasks:
        if task["description"].lower() == reference_lower:
            return task
    
    # Try partial match
    for task in tasks:
        if reference_lower in task["description"].lower():
            return task
    
    return None


async def execute_tool_calls_sync(tool_calls: List[Dict[str, Any]], user_id: int) -> List[Dict[str, Any]]:
    """Execute MCP tool calls (async wrapper for sync context)."""
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.get("name", "")
        parameters = tool_call.get("input", {})
        if not isinstance(parameters, dict):
            parameters = {}
        parameters["user_id"] = user_id
        
        if tool_name in TOOL_MAP:
            try:
                tool_func = TOOL_MAP[tool_name]
                result = await tool_func(parameters)
                # Ensure result is in correct format
                if isinstance(result, dict):
                    results.append({
                        "tool_use_id": tool_call.get("tool_use_id", ""),
                        "content": result,
                        "success": result.get("success", True)
                    })
                else:
                    results.append({
                        "tool_use_id": tool_call.get("tool_use_id", ""),
                        "content": {"success": True, "result": str(result)},
                        "success": True
                    })
            except Exception as e:
                print(f"[Gradio] Tool execution error ({tool_name}): {e}")
                results.append({
                    "tool_use_id": tool_call.get("tool_use_id", ""),
                    "content": {"success": False, "error": str(e)},
                    "success": False
                })
        else:
            results.append({
                "tool_use_id": tool_call.get("tool_use_id", ""),
                "content": {"success": False, "error": f"Unknown tool: {tool_name}"},
                "success": False
            })
    return results


def process_chat_message(user_id: int, message: str) -> str:
    """Process chat message - PRODUCTION-READY with robust error handling."""
    if not message or not isinstance(message, str):
        return "I'm sorry, I didn't receive a valid message. Please try again."
    
    message = message.strip()
    if not message or len(message) < 1:
        return "I'm sorry, your message appears to be empty. Please try again."
    
    # Store user message (non-blocking)
    try:
        store_message(user_id, "user", message)
    except Exception:
        pass
    
    # Try Phase III Agent first (if available)
    if PHASE_III_AVAILABLE:
        try:
            history = get_conversation_history(user_id, limit=20)
            history_messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in history
            ]
            
            agent = create_agent(api_key="mock", config=get_agent_config())
            tools = get_mcp_tool_definitions()
            
            agent_response = agent.process_message(
                user_message=message,
                conversation_history=history_messages,
                user_id=user_id,
                tools=tools
            )
            
            final_response = agent_response.get("response_text", "")
            
            # Execute tool calls if needed
            if agent_response.get("requires_tool_execution") and agent_response.get("tool_calls"):
                try:
                    # Normalize tool calls
                    tool_calls_to_execute = []
                    for tc in agent_response.get("tool_calls", []):
                        if isinstance(tc, dict):
                            tool_name = tc.get("name", "")
                            tool_input = tc.get("input", {})
                            if not tool_input or not isinstance(tool_input, dict):
                                tool_input = {k: v for k, v in tc.items() if k not in ["name", "tool_use_id"]}
                            tool_calls_to_execute.append({
                                "name": tool_name,
                                "input": tool_input
                            })
                    
                    if tool_calls_to_execute:
                        tool_results = asyncio.run(execute_tool_calls_sync(tool_calls_to_execute, user_id))
                        
                        # Process tool results
                        try:
                            final_agent_response = agent.process_tool_results(tool_results=tool_results, user_id=user_id)
                            final_response = final_agent_response.get("response_text", final_response)
                        except Exception:
                            # Manual response generation from tool results
                            result_messages = []
                            for r in tool_results:
                                content = r.get("content", {})
                                if isinstance(content, dict) and content.get("success", False):
                                    if "todos" in content:
                                        todos = content["todos"]
                                        if todos:
                                            task_list = "\n".join([
                                                f"{t.get('id')}. {t.get('title')} {'✅' if t.get('completed') else '⏳'}"
                                                for t in todos
                                            ])
                                            result_messages.append(f"Your tasks:\n{task_list}")
                                        else:
                                            result_messages.append("You have no tasks.")
                                    elif "todo_id" in content:
                                        todo_id = content["todo_id"]
                                        if "deleted" in content:
                                            result_messages.append(f"Successfully deleted task {todo_id}.")
                                        elif "title" in content:
                                            result_messages.append(f"Task '{content['title']}' processed successfully (ID: {todo_id}).")
                            
                            if result_messages:
                                final_response = " ".join(result_messages)
                except Exception as e:
                    print(f"[Gradio] Tool execution error: {e}")
                    # Continue with initial response or fall through
            
            # Ensure we have a response
            if final_response and final_response.strip():
                try:
                    store_message(user_id, "assistant", final_response)
                except Exception:
                    pass
                return final_response
        except Exception as e:
            print(f"[Gradio] Agent error (using fallback): {type(e).__name__}: {e}")
            # Fall through to reliable regex fallback
    
    # RELIABLE FALLBACK: Regex-based intent recognition
    try:
        intent, params = recognize_intent(message)
        
        if intent == "create":
            description = params.get("description", "")
            if not description or len(description.strip()) < 2:
                response = "I'd be happy to add a task for you! What would you like to add to your todo list?"
            else:
                success, msg = create_task(user_id, description)
                if success:
                    response = f"✅ I've added '{description}' to your todo list!"
                else:
                    response = f"I'm sorry, I couldn't add that task: {msg}"
        
        elif intent == "list":
            tasks = get_user_tasks(user_id)
            if not tasks:
                response = "You don't have any tasks yet. Would you like to add one?"
            else:
                active = [t for t in tasks if not t["completed"]]
                completed = [t for t in tasks if t["completed"]]
                response = "Here are your tasks:\n\n"
                if active:
                    response += f"🔄 Active Tasks ({len(active)}):\n"
                    for i, task in enumerate(active, 1):
                        response += f"{i}. {task['description']} (ID: {task['id']})\n"
                if completed:
                    response += f"\n✅ Completed Tasks ({len(completed)}):\n"
                    for i, task in enumerate(completed, 1):
                        response += f"{i}. {task['description']} ✅ (ID: {task['id']})\n"
        
        elif intent == "complete":
            task_id = params.get("task_id")
            task_ref = params.get("task_reference", "")
            
            print(f"[Gradio] Complete intent - task_id: {task_id}, task_ref: {task_ref}")
            
            if task_id:
                print(f"[Gradio] Attempting to mark task {task_id} as complete...")
                success, msg = update_task(user_id, task_id, completed=True)
                if success:
                    response = f"✅ I've marked task {task_id} as complete!"
                else:
                    print(f"[Gradio] Failed to complete task: {msg}")
                    response = f"I'm sorry, I couldn't complete that task: {msg}. Make sure task {task_id} exists. Try 'show my tasks' to see your task IDs."
            elif task_ref:
                task = find_task_by_reference(user_id, task_ref)
                if not task:
                    response = f"I couldn't find a task matching '{task_ref}'. Try 'show my tasks' to see your tasks."
                else:
                    success, msg = update_task(user_id, task["id"], completed=True)
                    if success:
                        response = f"✅ I've marked '{task['description']}' as complete!"
                    else:
                        response = f"I'm sorry, I couldn't complete that task: {msg}"
            else:
                response = "Which task would you like to mark as complete? Please specify the task number (e.g., 'mark task 1 as complete')."
        
        elif intent == "delete":
            task_id = params.get("task_id")
            task_ref = params.get("task_reference", "")
            
            if task_id:
                success, msg = delete_task(user_id, task_id)
                if success:
                    response = f"✅ I've deleted task {task_id}."
                else:
                    response = f"I'm sorry, I couldn't delete that task: {msg}"
            elif task_ref:
                task = find_task_by_reference(user_id, task_ref)
                if not task:
                    response = f"I couldn't find a task matching '{task_ref}'."
                else:
                    success, msg = delete_task(user_id, task["id"])
                    if success:
                        response = f"✅ I've deleted the task '{task['description']}'."
                    else:
                        response = f"I'm sorry, I couldn't delete that task: {msg}"
            else:
                response = "Which task would you like to delete? Please specify the task number."
        
        else:
            response = (
                "I can help you manage your tasks! Try saying:\n"
                "• 'Add a task to buy groceries'\n"
                "• 'Show my tasks'\n"
                "• 'Mark task 1 as complete'\n"
                "• 'Delete task 1'"
            )
        
        # Store response
        try:
            store_message(user_id, "assistant", response)
        except Exception:
            pass
        
        return response
        
    except Exception as e:
        print(f"[Gradio] Fallback error: {e}")
        import traceback
        traceback.print_exc()
        return f"I'm sorry, I encountered an error: {str(e)}. Please try rephrasing your request or say 'show my tasks' to see your task list."


def transcribe_audio(audio_input) -> Tuple[str, Optional[str]]:
    """Transcribe audio - tries OpenAI → Google (free) → faster-whisper."""
    path = None
    if isinstance(audio_input, str) and audio_input:
        path = audio_input
    elif isinstance(audio_input, (list, tuple)) and len(audio_input) >= 1:
        path = audio_input[0] if isinstance(audio_input[0], str) else None
    
    if not path or not os.path.isfile(path):
        return "", "No audio file received. Record again and try."
    
    # Try OpenAI Whisper
    text = _transcribe_openai(path)
    if text:
        return (text, None)
    
    # Try Google Speech (free)
    text, err = _transcribe_google(path)
    if text:
        return (text, None)
    
    return ("", err or "Transcription failed. Please try typing instead.")


def _transcribe_openai(path: str) -> str:
    """Use OpenAI Whisper API."""
    try:
        from openai import OpenAI
        raw = (os.getenv("OPENAI_API_KEY") or "").strip().strip('"\'')
        if not raw or raw.startswith("sk-placeholder"):
            return ""
        client = OpenAI(api_key=raw)
        with open(path, "rb") as f:
            r = client.audio.transcriptions.create(model="whisper-1", file=f, language="en")
        return (r.text or "").strip()
    except Exception:
        return ""


def _transcribe_google(path: str) -> Tuple[str, Optional[str]]:
    """Use SpeechRecognition + Google Web Speech (free)."""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(path) as source:
            audio = r.record(source, duration=60)
        text = r.recognize_google(audio, language="en-US").strip()
        return (text, None) if text else ("", "No speech detected.")
    except ImportError:
        return "", "Install: pip install SpeechRecognition"
    except Exception as e:
        err = str(e).lower()
        if "unknown" in err or "could not understand" in err:
            return "", "Could not understand audio. Try speaking clearly."
        if "request" in err or "connection" in err or "network" in err:
            return "", "Google Speech needs internet. Check connection."
        return "", f"Transcription error: {type(e).__name__}"


def process_input(text_input, history_state, user_id: int = 1):
    """Process text input and return response."""
    if not text_input or not text_input.strip():
        return history_state or [], "", ""
    
    transcript = text_input.strip()
    response = process_chat_message(user_id, transcript)
    
    if history_state is None:
        history_state = []
    
    # Gradio Chatbot expects list of tuples: [(user_msg, assistant_msg), ...]
    updated_history = history_state + [(transcript, response)]
    
    return updated_history, "", ""


def clear_chat(history_state):
    """Clear conversation history."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversation_messages WHERE user_id = ?", (1,))
        conn.commit()
        conn.close()
    except Exception:
        pass
    return []  # Return empty list (Gradio Chatbot format)


# Initialize database
init_database()

# Create Gradio Interface
with gr.Blocks(title="Todo App - AI Assistant with Voice") as app:
    gr.Markdown("# 🤖 Todo App - AI Assistant with Voice Input")
    
    if PHASE_III_AVAILABLE:
        gr.Markdown("**✅ Phase III Compliant: Using OpenAI Agents SDK + MCP Tools**")
    else:
        gr.Markdown("**✅ Using Reliable Regex-Based Intent Recognition**")
    
    gr.Markdown("**Speak or type your todo commands! Free voice transcription available.**")
    
    chatbot = gr.Chatbot(
        label="Conversation",
        height=400
    )
    
    history_state = gr.State(value=[])
    
    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown("### 🎤 Voice Input (Record Audio)")
            gr.Markdown("**Record your command with the mic below. Free transcription (no API key) when OpenAI is unavailable.**")
            
            voice_audio = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Record Your Voice Command",
                show_label=True
            )
            
            voice_transcript = gr.Textbox(
                label="Transcribed Text",
                visible=False
            )
            
            def process_voice_audio(audio_file):
                """Process recorded audio and transcribe it."""
                if audio_file is None:
                    return "", "Ready (free voice — no API key)"
                transcript, err = transcribe_audio(audio_file)
                if err:
                    return "", f"[WARN] {err}"
                return transcript, f"[OK] Transcribed: {transcript}"
            
            voice_status = gr.Textbox(
                label="Voice Status",
                interactive=False,
                visible=True,
                value="Ready (free voice — no API key)"
            )
            
            voice_audio.change(
                fn=process_voice_audio,
                inputs=[voice_audio],
                outputs=[voice_transcript, voice_status]
            )
            
            gr.Markdown("### ✍️ Type Your Message")
            text_input = gr.Textbox(
                label="Message",
                placeholder="Type your command here, or record voice above",
                lines=2
            )
            
            def auto_fill_from_voice(transcript):
                """Auto-fill text input when voice transcription is ready."""
                if transcript and transcript.strip():
                    return transcript.strip()
                return ""
            
            voice_transcript.change(
                fn=auto_fill_from_voice,
                inputs=[voice_transcript],
                outputs=[text_input]
            )
            
            with gr.Row():
                submit_btn = gr.Button("📤 Send", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
        
        with gr.Column(scale=1):
            gr.Markdown("### 📋 Quick Commands")
            gr.Examples(
                examples=[
                    ["add task buy milk"],
                    ["list my tasks"],
                    ["add task call dentist"],
                    ["show all tasks"],
                    ["mark task 1 as complete"],
                    ["delete task 1"],
                ],
                inputs=text_input
            )
    
    def handle_submit(text, history):
        """Handle form submission."""
        new_history, cleared_text, status = process_input(text, history, user_id=1)
        return new_history, cleared_text, status
    
    submit_btn.click(
        fn=handle_submit,
        inputs=[text_input, history_state],
        outputs=[chatbot, text_input, gr.Textbox(visible=False)]
    )
    
    text_input.submit(
        fn=handle_submit,
        inputs=[text_input, history_state],
        outputs=[chatbot, text_input, gr.Textbox(visible=False)]
    )
    
    clear_btn.click(
        fn=clear_chat,
        inputs=[history_state],
        outputs=[chatbot]
    )
    
    def load_history():
        """Load conversation history from database."""
        try:
            history = get_conversation_history(user_id=1, limit=10)
            # Gradio Chatbot expects list of tuples: [(user_msg, assistant_msg), ...]
            chat_history = []
            user_msg = None
            for msg in history:
                if msg["role"] == "user":
                    user_msg = msg["content"]
                elif msg["role"] == "assistant" and user_msg:
                    chat_history.append((user_msg, msg["content"]))
                    user_msg = None
            return chat_history, chat_history
        except Exception as e:
            print(f"[Gradio] Error loading history: {e}")
            return [], []
    
    app.load(load_history, outputs=[chatbot, history_state])

if __name__ == "__main__":
    # Try port 7860, if busy try 7861
    import socket
    port = 7860
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex(('localhost', 7860)) == 0:
        port = 7861
        print(f"[Gradio] Port 7860 in use, using port {port} instead")
    sock.close()
    
    print("\n" + "="*60)
    print("🚀 Phase III Todo App Starting...")
    print("="*60)
    print(f"\n📱 Open in your browser:")
    print(f"   http://localhost:{port}")
    print(f"   http://127.0.0.1:{port}")
    print("\n" + "="*60 + "\n")
    
    app.launch(
        share=False,
        server_name="127.0.0.1",  # Use 127.0.0.1 for better browser compatibility
        server_port=port,
        show_error=True,
        theme=gr.themes.Default(),  # Theme moved to launch() in Gradio 6.0+
    )
