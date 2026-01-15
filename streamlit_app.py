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

# Voice input imports
try:
    from audio_recorder_streamlit import audio_recorder
    AUDIO_RECORDER_AVAILABLE = True
except ImportError:
    AUDIO_RECORDER_AVAILABLE = False

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

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
    
    # Create task intent
    create_patterns = [
        r"add\s+(?:a\s+)?(?:task|todo|item)\s+(?:to|for|about)?\s*(?:.*?)(?:to\s+)?(.+)",
        r"create\s+(?:a\s+)?(?:task|todo|item)\s*(?:.*?)(?:to\s+)?(.+)",
        r"new\s+(?:task|todo|item)\s*(?:.*?)(?:to\s+)?(.+)",
        r"remind\s+me\s+(?:to\s+)?(.+)",
        r"i\s+need\s+(?:to\s+)?(.+)",
        r"add\s+(.+)",
        r"create\s+(.+)",
    ]
    
    # List tasks intent
    list_patterns = [
        r"show\s+(?:me\s+)?(?:all\s+)?(?:my\s+)?(?:tasks|todos|list)",
        r"list\s+(?:all\s+)?(?:my\s+)?(?:tasks|todos)",
        r"what\s+(?:are\s+)?(?:my\s+)?(?:tasks|todos)",
        r"display\s+(?:my\s+)?(?:tasks|todos)",
        r"view\s+(?:my\s+)?(?:tasks|todos)",
    ]
    
    # Complete task intent
    complete_patterns = [
        r"mark\s+(?:.*?)\s+(?:as\s+)?(?:done|complete|completed|finished)",
        r"complete\s+(?:.*?)(?:task|todo)?",
        r"(?:.*?)\s+is\s+(?:done|complete|completed|finished)",
        r"finish\s+(?:.*?)(?:task|todo)?",
        r"check\s+off\s+(.+)",
        r"done\s+with\s+(.+)",
    ]
    
    # Update task intent
    update_patterns = [
        r"change\s+(?:.*?)\s+to\s+(.+)",
        r"update\s+(?:.*?)\s+to\s+(.+)",
        r"modify\s+(?:.*?)\s+to\s+(.+)",
        r"edit\s+(?:.*?)\s+to\s+(.+)",
        r"rename\s+(?:.*?)\s+to\s+(.+)",
    ]
    
    # Delete task intent
    delete_patterns = [
        r"delete\s+(?:.*?)(?:task|todo)?",
        r"remove\s+(?:.*?)(?:task|todo)?",
        r"get\s+rid\s+of\s+(?:.*?)(?:task|todo)?",
        r"remove\s+(?:.*?)(?:task|todo)?",
    ]
    
    # Check for create intent
    for pattern in create_patterns:
        match = re.search(pattern, message_lower)
        if match:
            task_desc = match.group(1).strip() if match.groups() else message_lower.replace("add", "").replace("create", "").replace("new", "").replace("remind me to", "").replace("i need to", "").strip()
            if task_desc:
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
            return "complete", {"task_reference": task_ref or message_lower}
    
    # Check for update intent
    for pattern in update_patterns:
        match = re.search(pattern, message_lower)
        if match:
            new_desc = match.group(1).strip() if match.groups() else ""
            return "update", {"new_description": new_desc}
    
    # Check for delete intent
    for pattern in delete_patterns:
        if re.search(pattern, message_lower):
            return "delete", {"task_reference": message_lower}
    
    return "unknown", {}


def find_task_by_reference(user_id: int, reference: str) -> Optional[Dict]:
    """Find task by description reference."""
    tasks = get_user_tasks(user_id)
    reference_lower = reference.lower()
    for task in tasks:
        if reference_lower in task["description"].lower() or task["description"].lower() in reference_lower:
            return task
    # Try to find by ID
    if re.search(r"\d+", reference):
        task_id = int(re.search(r"\d+", reference).group())
        for task in tasks:
            if task["id"] == task_id:
                return task
    return None


def process_chat_message(user_id: int, message: str) -> str:
    """Process chat message and return AI response (Phase III)."""
    # Store user message
    store_message(user_id, "user", message)
    
    # Recognize intent
    intent, params = recognize_intent(message)
    
    try:
        if intent == "create":
            description = params.get("description", "")
            if not description:
                response = "I'd be happy to add a task for you! What would you like to add to your todo list?"
            else:
                success, msg = create_task(user_id, description)
                if success:
                    response = f"I've added '{description}' to your todo list. ✅"
                else:
                    response = f"I'm sorry, I couldn't add that task: {msg}"
        
        elif intent == "list":
            tasks = get_user_tasks(user_id)
            if not tasks:
                response = "You don't have any tasks yet. Would you like to add one?"
            else:
                active = [t for t in tasks if not t["completed"]]
                completed = [t for t in tasks if t["completed"]]
                response = f"Here are your tasks:\n\n"
                if active:
                    response += f"**Active Tasks ({len(active)}):**\n"
                    for i, task in enumerate(active, 1):
                        response += f"{i}. {task['description']}\n"
                if completed:
                    response += f"\n**Completed Tasks ({len(completed)}):**\n"
                    for i, task in enumerate(completed, 1):
                        response += f"{i}. ~~{task['description']}~~ ✅\n"
        
        elif intent == "complete":
            task_ref = params.get("task_reference", "")
            task = find_task_by_reference(user_id, task_ref)
            if not task:
                response = "I couldn't find that task. Would you like to see all your tasks?"
            else:
                if task["completed"]:
                    response = f"'{task['description']}' is already completed! ✅"
                else:
                    success, msg = update_task(user_id, task["id"], completed=True)
                    if success:
                        response = f"Great! I've marked '{task['description']}' as complete. Well done! ✅"
                    else:
                        response = f"I'm sorry, I couldn't complete that task: {msg}"
        
        elif intent == "update":
            new_desc = params.get("new_description", "")
            if not new_desc:
                response = "I'd be happy to update a task for you! Which task would you like to update, and what should the new description be?"
            else:
                # Try to find task from previous context or ask
                response = "Which task would you like to update? Please specify the task to change."
        
        elif intent == "delete":
            task_ref = params.get("task_reference", "")
            task = find_task_by_reference(user_id, task_ref)
            if not task:
                response = "I couldn't find that task to delete. Would you like to see all your tasks?"
            else:
                # For deletion, we'd normally ask for confirmation, but for simplicity, we'll delete
                success, msg = delete_task(user_id, task["id"])
                if success:
                    response = f"I've deleted '{task['description']}' from your todo list."
                else:
                    response = f"I'm sorry, I couldn't delete that task: {msg}"
        
        else:
            response = "I'm not sure I understood that. I can help you:\n- Add tasks (e.g., 'add task to buy groceries')\n- List your tasks (e.g., 'show my tasks')\n- Complete tasks (e.g., 'mark grocery task as done')\n- Delete tasks (e.g., 'delete grocery task')\n\nWhat would you like to do?"
    
    except Exception as e:
        response = "I'm sorry, I encountered an error processing your request. Please try again."
    
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
            history = get_conversation_history(st.session_state.user_id, limit=50)
            for msg in history:
                if msg["role"] == "user":
                    with st.chat_message("user"):
                        st.write(msg["content"])
                else:
                    with st.chat_message("assistant"):
                        st.markdown(msg["content"])
        
        # Voice input section (Phase III optional feature)
        st.markdown("---")
        st.subheader("🎤 Voice Input")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Text input
            if prompt := st.chat_input("Type your message here..."):
                # Process message
                response = process_chat_message(st.session_state.user_id, prompt)
                st.rerun()
        
        with col2:
            # Voice recorder
            if AUDIO_RECORDER_AVAILABLE and SPEECH_RECOGNITION_AVAILABLE:
                st.markdown("**Or use voice:**")
                audio_bytes = audio_recorder(
                    text="🎤 Click to record",
                    recording_color="#e74c3c",
                    neutral_color="#34495e",
                    icon_name="microphone",
                    icon_size="2x",
                    pause_threshold=2.0,
                    key="audio_recorder"
                )
                
                if audio_bytes:
                    # Process audio
                    with st.spinner("🎤 Processing your voice..."):
                        try:
                            # Save audio to temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                                tmp_file.write(audio_bytes)
                                tmp_file_path = tmp_file.name
                            
                            # Convert speech to text
                            recognizer = sr.Recognizer()
                            with sr.AudioFile(tmp_file_path) as source:
                                audio_data = recognizer.record(source)
                            
                            # Recognize speech
                            try:
                                voice_text = recognizer.recognize_google(audio_data)
                                st.success(f"🎤 Heard: *{voice_text}*")
                                
                                # Process the voice input as a chat message
                                if voice_text:
                                    response = process_chat_message(st.session_state.user_id, voice_text)
                                    st.rerun()
                            except sr.UnknownValueError:
                                st.error("🎤 Could not understand audio. Please try again.")
                            except sr.RequestError as e:
                                st.error(f"🎤 Speech recognition service error: {e}")
                            
                            # Clean up temp file
                            try:
                                os.unlink(tmp_file_path)
                            except:
                                pass
                                
                        except Exception as e:
                            st.error(f"🎤 Error processing audio: {str(e)}")
            else:
                st.info("🎤 Voice input requires additional packages. Install: `pip install streamlit-audio-recorder SpeechRecognition pydub`")
        
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
