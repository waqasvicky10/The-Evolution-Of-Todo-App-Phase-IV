"""
Phase II + Phase III Todo App - Streamlit
Complete implementation with:
- Phase II: Full-stack web app (10 User Stories)
- Phase III: AI-powered chatbot interface
- Natural language todo management
- Conversation history
- Dual interface (Traditional + Chat)
"""

import streamlit as st
import sqlite3
import bcrypt
import secrets
import re
import os
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict
import json
import base64
import io
import tempfile

# Voice input will use browser's Web Speech API (no Python packages needed)
VOICE_INPUT_AVAILABLE = True

# Page configuration
st.set_page_config(
    page_title="Todo App - Phase II & III",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database path
if os.path.exists("/tmp"):
    DB_PATH = "/tmp/todo.db"
elif os.path.exists("/mount/src"):
    DB_PATH = "/mount/src/todo.db"
else:
    DB_PATH = "todo.db"

ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)


def init_database():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
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
            completed BOOLEAN DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Refresh tokens table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS refresh_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Conversation messages table (Phase III)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user_id ON refresh_tokens(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_refresh_tokens_token ON refresh_tokens(token)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversation_user_id ON conversation_messages(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversation_created_at ON conversation_messages(created_at)")

    conn.commit()
    conn.close()


def get_db_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False


def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password according to Phase II requirements."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[^A-Za-z0-9]', password):
        return False, "Password must contain at least one special character"
    return True, ""


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def generate_token() -> str:
    """Generate secure random token."""
    return secrets.token_urlsafe(32)


def create_access_token(user_id: int) -> str:
    """Create access token (15 minutes lifetime)."""
    expires_at = datetime.now() + ACCESS_TOKEN_LIFETIME
    payload = {"user_id": user_id, "expires_at": expires_at.isoformat(), "type": "access"}
    token_data = base64.b64encode(json.dumps(payload).encode()).decode()
    return f"access_{token_data}"


def create_refresh_token(user_id: int) -> str:
    """Create refresh token (7 days lifetime)."""
    token = generate_token()
    expires_at = datetime.now() + REFRESH_TOKEN_LIFETIME
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM refresh_tokens WHERE user_id = ?", (user_id,))
    cursor.execute(
        "INSERT INTO refresh_tokens (user_id, token, expires_at, created_at) VALUES (?, ?, ?, ?)",
        (user_id, token, expires_at.isoformat(), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return token


def verify_access_token(token: str) -> Optional[int]:
    """Verify access token and return user_id if valid."""
    try:
        if not token.startswith("access_"):
            return None
        token_data = token[7:]
        payload = json.loads(base64.b64decode(token_data).decode())
        expires_at = datetime.fromisoformat(payload["expires_at"])
        if datetime.now() > expires_at:
            return None
        return payload.get("user_id")
    except Exception:
        return None


def verify_refresh_token(token: str) -> Optional[int]:
    """Verify refresh token."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, expires_at FROM refresh_tokens WHERE token = ?", (token,))
        result = cursor.fetchone()
        conn.close()
        if not result:
            return None
        user_id, expires_at_str = result
        expires_at = datetime.fromisoformat(expires_at_str)
        if datetime.now() > expires_at:
            return None
        return user_id
    except Exception:
        return None


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """Refresh access token using refresh token."""
    user_id = verify_refresh_token(refresh_token)
    if user_id:
        return create_access_token(user_id)
    return None


def register_user(email: str, password: str, password_confirm: str) -> Tuple[bool, str]:
    """Register a new user (US-201)."""
    if not email or not password or not password_confirm:
        return False, "All fields are required"
    if not validate_email(email):
        return False, "Please enter a valid email address"
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        return False, f"Password validation failed: {error_msg}"
    if password != password_confirm:
        return False, "Passwords do not match"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return False, "An account with this email already exists"
        password_hash = hash_password(password)
        now = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO users (email, password_hash, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (email.lower().strip(), password_hash, now, now)
        )
        conn.commit()
        conn.close()
        return True, "Registration successful! Please log in."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists"
    except Exception as e:
        return False, f"Registration failed. Please try again later."


def login_user(email: str, password: str) -> Tuple[bool, Optional[int], Optional[str], Optional[str], str]:
    """Login a user (US-202)."""
    if not email or not password:
        return False, None, None, None, "Email and password are required"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE email = ?", (email.lower().strip(),))
        user = cursor.fetchone()
        conn.close()
        if not user:
            return False, None, None, None, "Invalid email or password"
        user_id, password_hash = user
        if not verify_password(password, password_hash):
            return False, None, None, None, "Invalid email or password"
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)
        return True, user_id, access_token, refresh_token, "Login successful!"
    except Exception as e:
        return False, None, None, None, "Login failed. Please try again later."


def logout_user(refresh_token: str) -> bool:
    """Logout a user (US-203)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM refresh_tokens WHERE token = ?", (refresh_token,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return True


def get_user_tasks(user_id: int) -> list:
    """Get all tasks for a user (US-204)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, description, completed, created_at FROM tasks WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        )
        tasks = cursor.fetchall()
        conn.close()
        return [{"id": t[0], "description": t[1], "completed": bool(t[2]), "created_at": t[3]} for t in tasks]
    except Exception as e:
        return []


def create_task(user_id: int, description: str) -> Tuple[bool, str]:
    """Create a new task (US-205)."""
    if not description or not description.strip():
        return False, "Task description cannot be empty"
    if len(description) > 500:
        return False, "Task description too long (max 500 characters)"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO tasks (user_id, description, completed, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, description.strip(), False, now, now)
        )
        conn.commit()
        conn.close()
        return True, "Task created successfully!"
    except Exception as e:
        return False, f"Failed to create task. Please try again."


def update_task(user_id: int, task_id: int, description: Optional[str] = None, completed: Optional[bool] = None) -> Tuple[bool, str]:
    """Update a task (US-206, US-208)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        if not cursor.fetchone():
            conn.close()
            return False, "Task not found or access denied"
        updates = []
        params = []
        if description is not None:
            if not description.strip():
                conn.close()
                return False, "Task description cannot be empty"
            if len(description) > 500:
                conn.close()
                return False, "Task description too long (max 500 characters)"
            updates.append("description = ?")
            params.append(description.strip())
        if completed is not None:
            updates.append("completed = ?")
            params.append(completed)
        if not updates:
            conn.close()
            return False, "No changes to update"
        updates.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        params.append(task_id)
        params.append(user_id)
        cursor.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ? AND user_id = ?", params)
        conn.commit()
        conn.close()
        return True, "Task updated successfully!"
    except Exception as e:
        return False, f"Failed to update task. Please try again."


def delete_task(user_id: int, task_id: int) -> Tuple[bool, str]:
    """Delete a task (US-207)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        if not cursor.fetchone():
            conn.close()
            return False, "Task not found or access denied"
        cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        conn.commit()
        conn.close()
        return True, "Task deleted successfully!"
    except Exception as e:
        return False, f"Failed to delete task. Please try again."


def store_message(user_id: int, role: str, content: str) -> bool:
    """Store conversation message (Phase III)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversation_messages (user_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (user_id, role, content, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_conversation_history(user_id: int, limit: int = 20) -> List[Dict]:
    """Get conversation history (Phase III)."""
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


def clear_conversation_history(user_id: int) -> bool:
    """Clear conversation history."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversation_messages WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


# Phase III: Natural Language Intent Recognition
def recognize_intent(message: str) -> Tuple[str, Dict]:
    """Recognize user intent from natural language (Phase III)."""
    message_lower = message.lower().strip()
    
    # Create task intent - more flexible patterns
    create_patterns = [
        r"add\s+(?:a\s+)?(?:task|todo|item)\s+(?:to|for|about|by)?\s*(?:.*?)(?:to\s+)?(.+)",
        r"create\s+(?:a\s+)?(?:task|todo|item)\s*(?:.*?)(?:to\s+)?(.+)",
        r"new\s+(?:task|todo|item)\s*(?:.*?)(?:to\s+)?(.+)",
        r"remind\s+me\s+(?:to\s+)?(.+)",
        r"i\s+need\s+(?:to\s+)?(.+)",
        r"i\s+want\s+(?:to\s+)?(.+)",
        r"can\s+you\s+add\s+(.+)",
        r"please\s+add\s+(.+)",
        r"add\s+(.+)",
        r"create\s+(.+)",
        r"^(.+?)(?:\s+to\s+my\s+list|\s+as\s+a\s+task|\s+task)$",  # "buy milk to my list"
    ]
    
    # List tasks intent
    list_patterns = [
        r"show\s+(?:me\s+)?(?:all\s+)?(?:my\s+)?(?:tasks|todos|list)",
        r"list\s+(?:all\s+)?(?:my\s+)?(?:tasks|todos)",
        r"what\s+(?:are\s+)?(?:my\s+)?(?:tasks|todos)",
        r"display\s+(?:my\s+)?(?:tasks|todos)",
        r"view\s+(?:my\s+)?(?:tasks|todos)",
        r"get\s+(?:my\s+)?(?:tasks|todos)",
        r"see\s+(?:my\s+)?(?:tasks|todos)",
        r"what\s+do\s+i\s+have",
        r"what's\s+on\s+my\s+list",
    ]
    
    # Complete task intent
    complete_patterns = [
        r"mark\s+(.+?)\s+(?:as\s+)?(?:done|complete|completed|finished)",
        r"complete\s+(.+)",
        r"(.+?)\s+is\s+(?:done|complete|completed|finished)",
        r"finish\s+(.+)",
        r"check\s+off\s+(.+)",
        r"done\s+with\s+(.+)",
        r"done\s+(.+)",
        r"finish\s+(.+)",
        r"complete\s+(.+)",
    ]
    
    # Update task intent
    update_patterns = [
        r"change\s+(.+?)\s+to\s+(.+)",
        r"update\s+(.+?)\s+to\s+(.+)",
        r"modify\s+(.+?)\s+to\s+(.+)",
        r"edit\s+(.+?)\s+to\s+(.+)",
        r"rename\s+(.+?)\s+to\s+(.+)",
        r"change\s+(.+?)\s+from\s+(.+?)\s+to\s+(.+)",
    ]
    
    # Delete task intent
    delete_patterns = [
        r"delete\s+(.+)",
        r"remove\s+(.+)",
        r"get\s+rid\s+of\s+(.+)",
        r"erase\s+(.+)",
        r"cancel\s+(.+)",
    ]
    
    # Check for create intent
    for pattern in create_patterns:
        match = re.search(pattern, message_lower)
        if match:
            task_desc = match.group(1).strip() if match.groups() else ""
            # Fallback: extract description by removing common prefixes
            if not task_desc or len(task_desc) < 3:
                task_desc = message_lower
                for prefix in ["add", "create", "new", "remind me to", "i need to", "i want to", "can you add", "please add"]:
                    if task_desc.startswith(prefix):
                        task_desc = task_desc[len(prefix):].strip()
                        break
            # Clean up common suffixes
            task_desc = re.sub(r"\s+(?:to\s+my\s+list|as\s+a\s+task|task)$", "", task_desc, flags=re.IGNORECASE).strip()
            if task_desc and len(task_desc) > 2:
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
            if task_ref:
                return "complete", {"task_reference": task_ref}
    
    # Check for update intent
    for pattern in update_patterns:
        match = re.search(pattern, message_lower)
        if match:
            groups = match.groups()
            if len(groups) >= 2:
                task_ref = groups[0].strip()
                new_desc = groups[-1].strip()  # Last group is usually the new description
                return "update", {"task_reference": task_ref, "new_description": new_desc}
            elif len(groups) == 1:
                return "update", {"new_description": groups[0].strip()}
    
    # Check for delete intent
    for pattern in delete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            task_ref = match.group(1).strip() if match.groups() else ""
            if task_ref:
                return "delete", {"task_reference": task_ref}
    
    return "unknown", {}


def find_task_by_reference(user_id: int, reference: str) -> Optional[Dict]:
    """Find task by description reference with improved matching."""
    if not reference or not reference.strip():
        return None
    
    tasks = get_user_tasks(user_id)
    reference_lower = reference.lower().strip()
    
    # Try to find by ID first
    id_match = re.search(r"\d+", reference)
    if id_match:
        task_id = int(id_match.group())
        for task in tasks:
            if task["id"] == task_id:
                return task
    
    # Exact match
    for task in tasks:
        if task["description"].lower() == reference_lower:
            return task
    
    # Substring match (reference in task description)
    for task in tasks:
        if reference_lower in task["description"].lower():
            return task
    
    # Substring match (task description in reference)
    for task in tasks:
        task_desc_lower = task["description"].lower()
        if task_desc_lower in reference_lower and len(task_desc_lower) > 3:
            return task
    
    # Word-based matching (at least 2 words match)
    reference_words = set(reference_lower.split())
    if len(reference_words) >= 2:
        for task in tasks:
            task_words = set(task["description"].lower().split())
            common_words = reference_words.intersection(task_words)
            # If at least 2 significant words match
            significant_common = [w for w in common_words if len(w) > 2]
            if len(significant_common) >= 2:
                return task
    
    # Single word match (if reference is a single significant word)
    if len(reference_words) == 1:
        ref_word = list(reference_words)[0]
        if len(ref_word) > 3:
            for task in tasks:
                if ref_word in task["description"].lower().split():
                    return task
    
    return None


def process_chat_message(user_id: int, message: str) -> str:
    """Process chat message and return AI response (Phase III)."""
    # Validate and clean message
    if not message or not isinstance(message, str):
        return "I'm sorry, I didn't receive a valid message. Please try again."
    
    message = message.strip()
    if not message or len(message) < 1:
        return "I'm sorry, your message appears to be empty. Please try again."
    
    # Store user message
    try:
        store_message(user_id, "user", message)
    except Exception as e:
        # Log but continue processing - don't fail if storage fails
        pass
    
    # Get conversation history for context
    try:
        history = get_conversation_history(user_id, limit=5)
    except Exception:
        history = []
    
    # Recognize intent
    try:
        intent, params = recognize_intent(message)
    except Exception as e:
        # If intent recognition fails, treat as unknown
        intent, params = "unknown", {}
    
    try:
        if intent == "create":
            description = params.get("description", "")
            if not description or len(description.strip()) < 2:
                response = "I'd be happy to add a task for you! What would you like to add to your todo list?\n\nYou can say things like:\n- 'Add task to buy groceries'\n- 'Create a task for meeting'\n- 'Remind me to call mom'"
            else:
                success, msg = create_task(user_id, description)
                if success:
                    response = f"✅ I've added '{description}' to your todo list!"
                else:
                    response = f"I'm sorry, I couldn't add that task: {msg}"
        
        elif intent == "list":
            tasks = get_user_tasks(user_id)
            if not tasks:
                response = "You don't have any tasks yet. Would you like to add one? Just say something like 'Add task to buy groceries'."
            else:
                active = [t for t in tasks if not t["completed"]]
                completed = [t for t in tasks if t["completed"]]
                response = f"Here are your tasks:\n\n"
                if active:
                    response += f"**🔄 Active Tasks ({len(active)}):**\n"
                    for i, task in enumerate(active, 1):
                        response += f"{i}. {task['description']}\n"
                if completed:
                    response += f"\n**✅ Completed Tasks ({len(completed)}):**\n"
                    for i, task in enumerate(completed, 1):
                        response += f"{i}. ~~{task['description']}~~ ✅\n"
                if not active and not completed:
                    response = "You don't have any tasks yet."
        
        elif intent == "complete":
            task_ref = params.get("task_reference", "")
            if not task_ref:
                # Try to get from context or ask user
                response = "Which task would you like to mark as complete? You can say the task description or number."
            else:
                task = find_task_by_reference(user_id, task_ref)
                if not task:
                    # Show available tasks to help user
                    tasks = get_user_tasks(user_id)
                    active_tasks = [t for t in tasks if not t["completed"]]
                    if active_tasks:
                        response = f"I couldn't find a task matching '{task_ref}'. Here are your active tasks:\n\n"
                        for i, t in enumerate(active_tasks, 1):
                            response += f"{i}. {t['description']}\n"
                        response += "\nWhich one would you like to complete?"
                    else:
                        response = f"I couldn't find a task matching '{task_ref}'. You don't have any active tasks to complete."
                else:
                    if task["completed"]:
                        response = f"'{task['description']}' is already completed! ✅"
                    else:
                        success, msg = update_task(user_id, task["id"], completed=True)
                        if success:
                            response = f"✅ Great! I've marked '{task['description']}' as complete. Well done!"
                        else:
                            response = f"I'm sorry, I couldn't complete that task: {msg}"
        
        elif intent == "update":
            task_ref = params.get("task_reference", "")
            new_desc = params.get("new_description", "")
            
            if not new_desc:
                response = "I'd be happy to update a task for you! Please tell me which task to update and what the new description should be.\n\nExample: 'Change grocery task to buy organic groceries'"
            elif not task_ref:
                # Try to find from context or ask
                response = "Which task would you like to update? Please specify the task.\n\nExample: 'Change grocery task to buy organic groceries'"
            else:
                task = find_task_by_reference(user_id, task_ref)
                if not task:
                    tasks = get_user_tasks(user_id)
                    if tasks:
                        response = f"I couldn't find a task matching '{task_ref}'. Here are your tasks:\n\n"
                        for i, t in enumerate(tasks, 1):
                            response += f"{i}. {t['description']}\n"
                        response += "\nWhich one would you like to update?"
                    else:
                        response = f"I couldn't find a task matching '{task_ref}'. You don't have any tasks yet."
                else:
                    success, msg = update_task(user_id, task["id"], description=new_desc)
                    if success:
                        response = f"✅ I've updated '{task['description']}' to '{new_desc}'."
                    else:
                        response = f"I'm sorry, I couldn't update that task: {msg}"
        
        elif intent == "delete":
            task_ref = params.get("task_reference", "")
            if not task_ref:
                response = "Which task would you like to delete? Please specify the task description or number."
            else:
                task = find_task_by_reference(user_id, task_ref)
                if not task:
                    tasks = get_user_tasks(user_id)
                    if tasks:
                        response = f"I couldn't find a task matching '{task_ref}'. Here are your tasks:\n\n"
                        for i, t in enumerate(tasks, 1):
                            response += f"{i}. {t['description']}\n"
                        response += "\nWhich one would you like to delete?"
                    else:
                        response = f"I couldn't find a task matching '{task_ref}'. You don't have any tasks yet."
                else:
                    success, msg = delete_task(user_id, task["id"])
                    if success:
                        response = f"✅ I've deleted '{task['description']}' from your todo list."
                    else:
                        response = f"I'm sorry, I couldn't delete that task: {msg}"
        
        else:
            # Unknown intent - provide helpful suggestions
            tasks = get_user_tasks(user_id)
            response = "I'm not sure I understood that. I can help you with:\n\n"
            response += "**📝 Add tasks:**\n"
            response += "- 'Add task to buy groceries'\n"
            response += "- 'Create a task for meeting'\n"
            response += "- 'Remind me to call mom'\n\n"
            response += "**📋 List tasks:**\n"
            response += "- 'Show my tasks'\n"
            response += "- 'What are my todos'\n\n"
            response += "**✅ Complete tasks:**\n"
            response += "- 'Mark grocery task as done'\n"
            response += "- 'Complete task 1'\n\n"
            response += "**✏️ Update tasks:**\n"
            response += "- 'Change grocery task to buy organic groceries'\n\n"
            response += "**🗑️ Delete tasks:**\n"
            response += "- 'Delete grocery task'\n\n"
            if tasks:
                response += f"You currently have {len(tasks)} task(s). What would you like to do?"
            else:
                response += "You don't have any tasks yet. Would you like to add one?"
    
    except Exception as e:
        # Show actual error for debugging (in development)
        import traceback
        error_details = str(e)
        error_trace = traceback.format_exc()
        
        # Log error details (in production, you might want to log this instead)
        response = f"I'm sorry, I encountered an error processing your request.\n\n"
        response += f"Error: {error_details}\n\n"
        response += "Please try rephrasing your request or contact support if the issue persists."
        
        # For debugging - you can remove this in production
        # response += f"\n\nDebug info:\n{error_trace}"
    
    # Store AI response
    store_message(user_id, "assistant", response)
    return response


def check_authentication() -> Optional[int]:
    """Check if user is authenticated (US-210, US-209)."""
    if "access_token" not in st.session_state or not st.session_state.access_token:
        return None
    user_id = verify_access_token(st.session_state.access_token)
    if user_id is None and "refresh_token" in st.session_state and st.session_state.refresh_token:
        new_access_token = refresh_access_token(st.session_state.refresh_token)
        if new_access_token:
            st.session_state.access_token = new_access_token
            user_id = verify_access_token(new_access_token)
        else:
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            return None
    return user_id


# Initialize database
init_database()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "traditional"  # or "chat"

# Check authentication
authenticated_user_id = check_authentication()
if authenticated_user_id:
    st.session_state.logged_in = True
    st.session_state.user_id = authenticated_user_id
else:
    if st.session_state.logged_in:
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_email = None

# Main App Logic
if st.session_state.logged_in and st.session_state.user_id:
    # Sidebar
    with st.sidebar:
        st.title("✅ Todo App")
        st.markdown(f"**Welcome, {st.session_state.user_email}!**")
        
        # View mode selector
        st.markdown("---")
        st.subheader("View Mode")
        view_mode = st.radio(
            "Choose interface:",
            ["Traditional", "AI Chat"],
            index=0 if st.session_state.view_mode == "traditional" else 1,
            key="view_mode_radio"
        )
        st.session_state.view_mode = view_mode.lower().replace(" ", "_")
        
        st.markdown("---")
        if st.button("🚪 Logout", type="secondary", use_container_width=True, key="logout_btn"):
            if st.session_state.refresh_token:
                logout_user(st.session_state.refresh_token)
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            st.session_state.page = "login"
            st.session_state.view_mode = "traditional"
            st.rerun()
    
    # Main content area
    if st.session_state.view_mode == "ai_chat":
        # Phase III: AI Chat Interface
        st.title("🤖 AI Todo Assistant")
        st.markdown("**Chat with me to manage your todos naturally!**")
        st.markdown("Try saying: 'Add task to buy groceries', 'Show my tasks', 'Mark grocery task as done'")
        
        # Chat interface
        chat_container = st.container()
        with chat_container:
            # Display conversation history
            try:
                history = get_conversation_history(st.session_state.user_id, limit=50)
                if history:
                    for msg in history:
                        if msg["role"] == "user":
                            with st.chat_message("user"):
                                st.write(msg["content"])
                        else:
                            with st.chat_message("assistant"):
                                st.markdown(msg["content"])
                else:
                    # Show welcome message if no history
                    with st.chat_message("assistant"):
                        st.markdown("👋 Hi! I'm your AI Todo Assistant. I can help you:\n\n- **Add tasks** (e.g., 'Add task to buy groceries')\n- **List tasks** (e.g., 'Show my tasks')\n- **Complete tasks** (e.g., 'Mark grocery task as done')\n- **Update tasks** (e.g., 'Change grocery task to buy organic groceries')\n- **Delete tasks** (e.g., 'Delete grocery task')\n\nTry typing a command or use voice input below!")
            except Exception as e:
                st.error(f"Error loading conversation history: {str(e)}")
                with st.chat_message("assistant"):
                    st.markdown("👋 Hi! I'm your AI Todo Assistant. How can I help you today?")
        
        # Voice input section (Phase III optional feature)
        st.markdown("---")
        st.subheader("🎤 Voice Input")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Text input
            st.markdown("**Type your message:**")
            if prompt := st.chat_input("Type your message here..."):
                # Validate prompt
                if not prompt or not prompt.strip():
                    st.warning("Please enter a message.")
                    st.rerun()
                
                # Process message
                try:
                    with st.spinner("🤔 Processing your message..."):
                        # Store user message immediately for display
                        with st.chat_message("user"):
                            st.write(prompt)
                        
                        # Process and get response
                        response = process_chat_message(st.session_state.user_id, prompt.strip())
                        
                        # Display response immediately
                        with st.chat_message("assistant"):
                            st.markdown(response)
                    
                    # Force rerun to refresh conversation history
                    st.rerun()
                except Exception as e:
                    error_msg = str(e)
                    st.error(f"❌ Error processing message: {error_msg}")
                    
                    # Show error in chat
                    with st.chat_message("assistant"):
                        st.error(f"I encountered an error: {error_msg}\n\nPlease try rephrasing your request or try again.")
                    
                    import traceback
                    with st.expander("🔍 Error details (click to expand)"):
                        st.code(traceback.format_exc())
                    
                    # Still rerun to show error
                    st.rerun()
        
        with col2:
            # Voice input using browser's Web Speech API
            if VOICE_INPUT_AVAILABLE:
                st.markdown("**Or use voice:**")
                
                # Initialize voice input state
                if "voice_text_result" not in st.session_state:
                    st.session_state.voice_text_result = ""
                if "voice_auto_submit" not in st.session_state:
                    st.session_state.voice_auto_submit = False
                
                # Voice input text field (will be filled by JavaScript)
                voice_text_input = st.text_input(
                    "Voice input will appear here (then click Submit)",
                    value=st.session_state.voice_text_result,
                    key="voice_text_input",
                    placeholder="Click voice button and speak, then click Submit..."
                )
                
                # Submit button for voice input
                if st.button("📤 Submit Voice Input", key="submit_voice", use_container_width=True, disabled=not voice_text_input.strip()):
                    if voice_text_input and voice_text_input.strip():
                        voice_text = voice_text_input.strip()
                        # Display in chat immediately
                        with st.chat_message("user"):
                            st.write(voice_text)
                        
                        try:
                            with st.spinner("🤔 Processing your voice command..."):
                                response = process_chat_message(st.session_state.user_id, voice_text)
                            
                            # Display response
                            with st.chat_message("assistant"):
                                st.markdown(response)
                            
                            # Clear voice input
                            st.session_state.voice_text_result = ""
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error processing voice input: {str(e)}")
                            import traceback
                            with st.expander("🔍 Error details (click to expand)"):
                                st.code(traceback.format_exc())
                            st.session_state.voice_text_result = ""
                            st.rerun()
                
                # Create HTML/JS component for voice input (no navigation, just fills input)
                voice_html = """
                <div style="margin: 10px 0;">
                    <button id="voiceBtn" onclick="startVoiceRecognition()" 
                            style="background-color: #e74c3c; color: white; border: none; 
                                   padding: 10px 20px; border-radius: 5px; cursor: pointer;
                                   font-size: 16px; width: 100%;">
                        🎤 Click to Record Voice
                    </button>
                    <div id="voiceStatus" style="margin-top: 10px; color: #666; font-size: 14px; min-height: 20px;"></div>
                </div>
                
                <script>
                (function() {
                    let recognition = null;
                    let isRecording = false;
                    
                    window.startVoiceRecognition = function() {
                        const btn = document.getElementById('voiceBtn');
                        const status = document.getElementById('voiceStatus');
                        
                        if (!btn || !status) {
                            console.error('Voice button or status element not found');
                            return;
                        }
                        
                        if (isRecording) {
                            if (recognition) {
                                recognition.stop();
                            }
                            isRecording = false;
                            btn.textContent = '🎤 Click to Record Voice';
                            btn.style.backgroundColor = '#e74c3c';
                            status.innerHTML = '<span style="color: orange;">⏹️ Stopped recording</span>';
                            return;
                        }
                        
                        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                            status.innerHTML = '<span style="color: red;">❌ Speech recognition not supported. Please use Chrome, Edge, or Safari.</span>';
                            return;
                        }
                        
                        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                        recognition = new SpeechRecognition();
                        recognition.continuous = false;
                        recognition.interimResults = false;
                        recognition.lang = 'en-US';
                        
                        isRecording = true;
                        btn.textContent = '🎤 Listening... (Click to stop)';
                        btn.style.backgroundColor = '#27ae60';
                        status.innerHTML = '<span style="color: green;">🎤 Listening... Speak now!</span>';
                        
                        recognition.onresult = function(event) {
                            const transcript = event.results[0][0].transcript.trim();
                            status.innerHTML = '<span style="color: green;">✅ Heard: ' + transcript + '</span>';
                            
                            // Try to fill the text input using postMessage (safe for sandboxed iframes)
                            try {
                                // Send message to parent window
                                if (window.parent && window.parent !== window) {
                                    window.parent.postMessage({
                                        type: 'voice_input',
                                        text: transcript
                                    }, '*');
                                }
                                
                                // Also try to find and fill input in current frame
                                setTimeout(function() {
                                    try {
                                        // Look for input fields in the parent document
                                        const parentDoc = window.parent.document;
                                        if (parentDoc) {
                                            const inputs = parentDoc.querySelectorAll('input[type="text"], input[placeholder*="Voice"], input[data-testid*="text_input"]');
                                            for (let i = 0; i < inputs.length; i++) {
                                                const input = inputs[i];
                                                if (input.placeholder && input.placeholder.includes('Voice')) {
                                                    input.value = transcript;
                                                    input.dispatchEvent(new Event('input', { bubbles: true }));
                                                    input.dispatchEvent(new Event('change', { bubbles: true }));
                                                    break;
                                                }
                                            }
                                        }
                                    } catch (e) {
                                        console.log('Could not fill input directly:', e);
                                    }
                                }, 100);
                                
                                status.innerHTML += '<br><span style="color: blue;">💡 Text filled! Click "Submit Voice Input" button above.</span>';
                            } catch (e) {
                                console.error('Error setting voice input:', e);
                                status.innerHTML += '<br><span style="color: orange;">⚠️ Please copy this text and paste it: ' + transcript + '</span>';
                            }
                        };
                        
                        recognition.onerror = function(event) {
                            status.innerHTML = '<span style="color: red;">❌ Error: ' + event.error + '</span>';
                            btn.textContent = '🎤 Click to Record Voice';
                            btn.style.backgroundColor = '#e74c3c';
                            isRecording = false;
                        };
                        
                        recognition.onend = function() {
                            btn.textContent = '🎤 Click to Record Voice';
                            btn.style.backgroundColor = '#e74c3c';
                            isRecording = false;
                            if (!status.innerHTML.includes('Heard:')) {
                                status.innerHTML = '<span style="color: orange;">⚠️ Recognition ended. Please try again.</span>';
                            }
                        };
                        
                        recognition.start();
                    };
                    
                    // Listen for messages from iframe (if needed)
                    window.addEventListener('message', function(event) {
                        if (event.data && event.data.type === 'voice_input') {
                            console.log('Received voice input:', event.data.text);
                        }
                    });
                })();
                </script>
                """
                
                # Use components.v1.html
                st.components.v1.html(voice_html, height=180)
                
                # Listen for postMessage from iframe (alternative method)
                # Note: This won't work directly, so we rely on the text input being filled
                # and the user clicking submit, or we use URL parameters as fallback
                
                # Check for voice input from URL parameters (fallback method)
                query_params = st.query_params
                if "voice_input" in query_params:
                    voice_text = query_params.get("voice_input", "").strip()
                    if voice_text:
                        # Set the voice text result
                        st.session_state.voice_text_result = voice_text
                        # Clear the parameter
                        new_params = {k: v for k, v in query_params.items() if k != "voice_input" and k != "_voice_timestamp"}
                        st.query_params = new_params
                        st.rerun()
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", key="clear_chat_btn"):
            clear_conversation_history(st.session_state.user_id)
            st.success("Chat history cleared!")
            st.rerun()

    else:
        # Phase II: Traditional Interface
        st.title("✅ My Todo List")
        st.markdown("**Manage your tasks with the traditional interface**")
        
        st.markdown("---")
        
        # Create new task (US-205)
        with st.form("create_task_form", clear_on_submit=True):
            st.subheader("➕ Add New Task")
            task_description = st.text_input("Task Description", placeholder="Enter your task here...", max_chars=500, key="create_task_input")
            submit_task = st.form_submit_button("Add Task", type="primary", use_container_width=True)
            
            if submit_task:
                if task_description and task_description.strip():
                    success, message = create_task(st.session_state.user_id, task_description)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Task description cannot be empty")

        st.markdown("---")

        # Display tasks (US-204)
        tasks = get_user_tasks(st.session_state.user_id)
        
        if tasks:
            st.subheader(f"📋 Your Tasks ({len(tasks)} total)")
            
            # Active tasks
            active_tasks = [t for t in tasks if not t["completed"]]
            if active_tasks:
                st.markdown("### 🔄 Active Tasks")
                for task in active_tasks:
                    with st.container():
                        col1, col2, col3, col4 = st.columns([1, 8, 1, 1])
                        with col1:
                            if st.button("✅", key=f"complete_{task['id']}", help="Mark as complete"):
                                update_task(st.session_state.user_id, task["id"], completed=True)
                                st.rerun()
                        with col2:
                            st.write(f"**{task['description']}**")
                        with col3:
                            if st.button("✏️", key=f"edit_{task['id']}", help="Edit task"):
                                st.session_state[f"editing_{task['id']}"] = True
                                st.rerun()
                        with col4:
                            if st.button("🗑️", key=f"delete_{task['id']}", help="Delete task"):
                                delete_task(st.session_state.user_id, task["id"])
                                st.rerun()
                        
                        # Edit form (US-206)
                        if st.session_state.get(f"editing_{task['id']}", False):
                            with st.form(f"edit_form_{task['id']}"):
                                new_description = st.text_input("Edit Task", value=task["description"], key=f"edit_input_{task['id']}", max_chars=500)
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.form_submit_button("💾 Save", use_container_width=True):
                                        success, msg = update_task(st.session_state.user_id, task["id"], description=new_description)
                                        if success:
                                            st.session_state[f"editing_{task['id']}"] = False
                                            st.rerun()
                                        else:
                                            st.error(msg)
                                with col2:
                                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                                        st.session_state[f"editing_{task['id']}"] = False
                                        st.rerun()
                        st.markdown("---")
            
            # Completed tasks
            completed_tasks = [t for t in tasks if t["completed"]]
            if completed_tasks:
                st.markdown("### ✅ Completed Tasks")
                for task in completed_tasks:
                    with st.container():
                        col1, col2, col3, col4 = st.columns([1, 8, 1, 1])
                        with col1:
                            if st.button("↩️", key=f"undo_{task['id']}", help="Mark as incomplete"):
                                update_task(st.session_state.user_id, task["id"], completed=False)
                                st.rerun()
                        with col2:
                            st.write(f"~~{task['description']}~~")
                        with col3:
                            if st.button("✏️", key=f"edit_c_{task['id']}", help="Edit task"):
                                st.session_state[f"editing_{task['id']}"] = True
                                st.rerun()
                        with col4:
                            if st.button("🗑️", key=f"delete_c_{task['id']}", help="Delete task"):
                                delete_task(st.session_state.user_id, task["id"])
                                st.rerun()
                        
                        # Edit form for completed tasks
                        if st.session_state.get(f"editing_{task['id']}", False):
                            with st.form(f"edit_form_c_{task['id']}"):
                                new_description = st.text_input("Edit Task", value=task["description"], key=f"edit_input_c_{task['id']}", max_chars=500)
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.form_submit_button("💾 Save", use_container_width=True):
                                        success, msg = update_task(st.session_state.user_id, task["id"], description=new_description)
                                        if success:
                                            st.session_state[f"editing_{task['id']}"] = False
                                            st.rerun()
                                        else:
                                            st.error(msg)
                                with col2:
                                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                                        st.session_state[f"editing_{task['id']}"] = False
                                        st.rerun()
                        st.markdown("---")
        else:
            st.info("📝 No tasks yet. Create your first task above!")
    
else:
    # Login/Register
    if st.session_state.page == "signup":
        st.title("📝 Sign Up")
        st.markdown("**Create your account to start managing your todos**")
        
        with st.form("signup_form"):
            email = st.text_input("Email", placeholder="your.email@example.com", key="signup_email")
            password = st.text_input("Password", type="password", placeholder="At least 8 characters with uppercase, lowercase, number, and special character", key="signup_password")
            password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")
            submit = st.form_submit_button("Sign Up", type="primary", use_container_width=True)
            
            if submit:
                success, message = register_user(email, password, password_confirm)
                if success:
                    st.success(message)
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error(message)
        
        if st.button("← Back to Login", key="back_to_login_btn"):
            st.session_state.page = "login"
            st.rerun()
    
    else:
        st.session_state.page = "login"
        st.title("🔐 Login")
        st.markdown("**Sign in to access your todo list**")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your.email@example.com", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submit:
                success, user_id, access_token, refresh_token, message = login_user(email, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.user_email = email
                    st.session_state.access_token = access_token
                    st.session_state.refresh_token = refresh_token
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        if st.button("📝 Don't have an account? Sign up", key="signup_link_btn"):
            st.session_state.page = "signup"
            st.rerun()

# Footer
st.markdown("---")
st.markdown("**Phase II + Phase III Todo App** | Traditional UI + AI Chat | Built with Streamlit")
