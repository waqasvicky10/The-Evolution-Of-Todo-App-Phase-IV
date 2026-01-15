"""
Phase II Todo App - Streamlit
A complete, production-ready todo application implementing all Phase II requirements:
- User registration and authentication
- JWT-like session management
- Task CRUD operations
- User data isolation
- Comprehensive error handling
- All 10 User Stories (US-201 to US-210)
"""

import streamlit as st
import sqlite3
import bcrypt
import secrets
import re
import os
from datetime import datetime, timedelta
from typing import Optional, Tuple
import json
import base64

# Page configuration
st.set_page_config(
    page_title="Todo App - Phase II",
    page_icon="✅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Database path - use writable location for Streamlit Cloud
if os.path.exists("/tmp"):
    DB_PATH = "/tmp/todo.db"
elif os.path.exists("/mount/src"):
    DB_PATH = "/mount/src/todo.db"
else:
    DB_PATH = "todo.db"

# Token expiration times (matching Phase II spec)
ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)


def init_database():
    """Initialize the SQLite database with users, tasks, and tokens tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Create tasks table
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

    # Create refresh tokens table (for token management)
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

    # Create indexes for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user_id ON refresh_tokens(user_id)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_refresh_tokens_token ON refresh_tokens(token)
    """)

    conn.commit()
    conn.close()


def get_db_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt (Phase II requirement)."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password according to Phase II requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    - Contains at least one special character
    """
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
    """Generate a secure random token."""
    return secrets.token_urlsafe(32)


def create_access_token(user_id: int) -> str:
    """Create a JWT-like access token (15 minutes lifetime)."""
    expires_at = datetime.now() + ACCESS_TOKEN_LIFETIME
    payload = {
        "user_id": user_id,
        "expires_at": expires_at.isoformat(),
        "type": "access"
    }
    token_data = base64.b64encode(json.dumps(payload).encode()).decode()
    return f"access_{token_data}"


def create_refresh_token(user_id: int) -> str:
    """Create a refresh token (7 days lifetime) and store it in database."""
    token = generate_token()
    expires_at = datetime.now() + REFRESH_TOKEN_LIFETIME
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clean up old tokens for this user
    cursor.execute("DELETE FROM refresh_tokens WHERE user_id = ?", (user_id,))
    
    # Insert new token
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
        
        token_data = token[7:]  # Remove "access_" prefix
        payload = json.loads(base64.b64decode(token_data).decode())
        
        expires_at = datetime.fromisoformat(payload["expires_at"])
        if datetime.now() > expires_at:
            return None
        
        return payload.get("user_id")
    except Exception:
        return None


def verify_refresh_token(token: str) -> Optional[int]:
    """Verify refresh token and return user_id if valid."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, expires_at FROM refresh_tokens WHERE token = ?",
            (token,)
        )
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
    """
    Register a new user (US-201).
    Returns (success, message).
    """
    # Validation
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
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return False, "An account with this email already exists"
        
        # Create new user
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
        return False, f"Registration failed. Please try again later. ({str(e)})"


def login_user(email: str, password: str) -> Tuple[bool, Optional[int], Optional[str], Optional[str], str]:
    """
    Login a user (US-202).
    Returns (success, user_id, access_token, refresh_token, message).
    """
    if not email or not password:
        return False, None, None, None, "Email and password are required"
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE email = ?", (email.lower().strip(),))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            # Generic error for security (US-202 requirement)
            return False, None, None, None, "Invalid email or password"
        
        user_id, password_hash = user
        if not verify_password(password, password_hash):
            # Generic error for security (US-202 requirement)
            return False, None, None, None, "Invalid email or password"
        
        # Create tokens
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)
        
        return True, user_id, access_token, refresh_token, "Login successful!"
    except Exception as e:
        return False, None, None, None, f"Login failed. Please try again later. ({str(e)})"


def logout_user(refresh_token: str) -> bool:
    """
    Logout a user by invalidating refresh token (US-203).
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM refresh_tokens WHERE token = ?", (refresh_token,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return True  # Always succeed, even if token doesn't exist


def get_user_tasks(user_id: int) -> list:
    """
    Get all tasks for a user (US-204).
    """
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
        st.error(f"Error loading tasks: {str(e)}")
        return []


def create_task(user_id: int, description: str) -> Tuple[bool, str]:
    """
    Create a new task (US-205).
    """
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
        return False, f"Failed to create task. Please try again. ({str(e)})"


def update_task(user_id: int, task_id: int, description: Optional[str] = None, completed: Optional[bool] = None) -> Tuple[bool, str]:
    """
    Update a task (US-206, US-208).
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify task belongs to user (security requirement)
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
        
        cursor.execute(
            f"UPDATE tasks SET {', '.join(updates)} WHERE id = ? AND user_id = ?",
            params
        )
        conn.commit()
        conn.close()
        return True, "Task updated successfully!"
    except Exception as e:
        return False, f"Failed to update task. Please try again. ({str(e)})"


def delete_task(user_id: int, task_id: int) -> Tuple[bool, str]:
    """
    Delete a task (US-207).
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify task belongs to user (security requirement)
        cursor.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        if not cursor.fetchone():
            conn.close()
            return False, "Task not found or access denied"
        
        cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        conn.commit()
        conn.close()
        return True, "Task deleted successfully!"
    except Exception as e:
        return False, f"Failed to delete task. Please try again. ({str(e)})"


def check_authentication() -> Optional[int]:
    """
    Check if user is authenticated (US-210).
    Returns user_id if authenticated, None otherwise.
    Handles token refresh automatically (US-209).
    """
    if "access_token" not in st.session_state or not st.session_state.access_token:
        return None
    
    user_id = verify_access_token(st.session_state.access_token)
    
    # If access token expired, try to refresh (US-209)
    if user_id is None and "refresh_token" in st.session_state and st.session_state.refresh_token:
        new_access_token = refresh_access_token(st.session_state.refresh_token)
        if new_access_token:
            st.session_state.access_token = new_access_token
            user_id = verify_access_token(new_access_token)
        else:
            # Refresh token expired, logout
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

# Check authentication status
authenticated_user_id = check_authentication()
if authenticated_user_id:
    st.session_state.logged_in = True
    st.session_state.user_id = authenticated_user_id
else:
    if st.session_state.logged_in:
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_email = None

# Get query params for navigation
query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"]

# Main App Logic
if st.session_state.logged_in and st.session_state.user_id:
    # User is logged in - show dashboard (US-204)
    st.title("✅ My Todo List")
    st.markdown(f"**Welcome, {st.session_state.user_email}!**")
    
    # Logout button (US-203)
    if st.button("🚪 Logout", type="secondary", key="logout_btn"):
        if st.session_state.refresh_token:
            logout_user(st.session_state.refresh_token)
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_email = None
        st.session_state.access_token = None
        st.session_state.refresh_token = None
        st.session_state.page = "login"
        st.rerun()
    
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
                    
                    # Edit form for completed tasks (US-206)
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
    # User is not logged in - show login/register (US-210: Protected Route Access Control)
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
st.markdown("**Phase II Todo App** | Built with Streamlit | All 10 User Stories Implemented")
