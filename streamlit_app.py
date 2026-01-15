"""
Simple Todo App - Streamlit
A clean, user-friendly todo application with authentication and task management.
No API keys required - works entirely with local database.
"""

import streamlit as st
import sqlite3
import hashlib
import os
from datetime import datetime
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="Todo App",
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


def init_database():
    """Initialize the SQLite database with users and tasks tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
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

    # Create index for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)
    """)

    conn.commit()
    conn.close()


def get_db_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)


def hash_password(password: str) -> str:
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == password_hash


def register_user(email: str, password: str) -> tuple[bool, str]:
    """Register a new user."""
    if not email or not password:
        return False, "Email and password are required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address"
    
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
        created_at = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
            (email, password_hash, created_at)
        )
        conn.commit()
        conn.close()
        return True, "Registration successful! Please log in."
    except Exception as e:
        return False, f"Registration failed: {str(e)}"


def login_user(email: str, password: str) -> tuple[bool, Optional[int], str]:
    """Login a user and return user_id if successful."""
    if not email or not password:
        return False, None, "Email and password are required"
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return False, None, "Invalid email or password"
        
        user_id, password_hash = user
        if verify_password(password, password_hash):
            return True, user_id, "Login successful!"
        else:
            return False, None, "Invalid email or password"
    except Exception as e:
        return False, None, f"Login failed: {str(e)}"


def get_user_tasks(user_id: int) -> list:
    """Get all tasks for a user."""
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


def create_task(user_id: int, description: str) -> tuple[bool, str]:
    """Create a new task."""
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
        return False, f"Failed to create task: {str(e)}"


def update_task(user_id: int, task_id: int, description: Optional[str] = None, completed: Optional[bool] = None) -> tuple[bool, str]:
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
        return False, f"Failed to update task: {str(e)}"


def delete_task(user_id: int, task_id: int) -> tuple[bool, str]:
    """Delete a task."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify task belongs to user
        cursor.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        if not cursor.fetchone():
            conn.close()
            return False, "Task not found"
        
        cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        conn.commit()
        conn.close()
        return True, "Task deleted successfully!"
    except Exception as e:
        return False, f"Failed to delete task: {str(e)}"


# Initialize database
init_database()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "page" not in st.session_state:
    st.session_state.page = "login"

# Get query params for navigation
query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"]

# Main App Logic
if st.session_state.logged_in:
    # User is logged in - show dashboard
    st.title("✅ My Todo List")
    st.markdown(f"**Welcome, {st.session_state.user_email}!**")
    
    # Logout button
    if st.button("🚪 Logout", type="secondary", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_email = None
        st.session_state.page = "login"
        st.rerun()
    
    st.markdown("---")
    
    # Create new task
    with st.form("create_task_form", clear_on_submit=True):
        st.subheader("➕ Add New Task")
        task_description = st.text_input("Task Description", placeholder="Enter your task here...", max_chars=500)
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
                st.error("Please enter a task description")
    
    st.markdown("---")
    
    # Display tasks
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
                    
                    # Edit form
                    if st.session_state.get(f"editing_{task['id']}", False):
                        with st.form(f"edit_form_{task['id']}"):
                            new_description = st.text_input("Edit Task", value=task["description"], key=f"edit_input_{task['id']}")
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
                            new_description = st.text_input("Edit Task", value=task["description"], key=f"edit_input_c_{task['id']}")
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
    # User is not logged in - show login/register
    if st.session_state.page == "signup":
        st.title("📝 Sign Up")
        
        with st.form("signup_form"):
            email = st.text_input("Email", placeholder="your.email@example.com", key="signup_email")
            password = st.text_input("Password", type="password", placeholder="At least 8 characters", key="signup_password")
            password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")
            submit = st.form_submit_button("Sign Up", type="primary", use_container_width=True)
            
            if submit:
                if password != password_confirm:
                    st.error("Passwords do not match")
                else:
                    success, message = register_user(email, password)
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
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your.email@example.com", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submit:
                success, user_id, message = login_user(email, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.user_email = email
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        if st.button("📝 Don't have an account? Sign up", key="signup_link_btn"):
            st.session_state.page = "signup"
            st.rerun()

# Footer
st.markdown("---")
st.markdown("**Simple Todo App** | Built with Streamlit")
