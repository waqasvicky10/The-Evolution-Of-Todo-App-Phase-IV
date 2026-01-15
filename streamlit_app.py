"""
Phase III Todo Chat App - Streamlit Deployment
AI-Powered Todo Assistant (Mock Mode - No API Key Required)

This is a user-friendly todo chat app that works without any API keys.
Uses intelligent pattern matching to understand your commands.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add phase_iii to path so imports work
project_root = Path(__file__).parent.absolute()
phase_iii_path = project_root / "phase_iii"
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(phase_iii_path) not in sys.path:
    sys.path.insert(0, str(phase_iii_path))

# Page configuration
st.set_page_config(
    page_title="Todo Chat - AI Assistant",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = 1  # Default user for demo
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Database path - use writable location for Streamlit Cloud
if os.path.exists("/tmp"):
    DB_PATH = "/tmp/todo.db"
elif os.path.exists("/mount/src"):
    DB_PATH = "/mount/src/todo.db"
else:
    DB_PATH = "todo.db"

# Set database path in environment
os.environ["DATABASE_PATH"] = DB_PATH

# Ensure MockProvider is used (no API key needed)
os.environ.pop("OPENAI_API_KEY", None)

# Initialize database tables
try:
    from phase_iii.persistence.repositories.conversation_repo import init_conversation_tables
    from phase_iii.persistence.repositories.tool_call_repo import init_tool_call_tables
    from phase_iii.mcp_server.tools.todo_tools import init_todo_tables
    
    # Update database path in modules
    import phase_iii.persistence.repositories.conversation_repo as conv_repo
    import phase_iii.mcp_server.tools.todo_tools as todo_tools
    conv_repo.DATABASE_PATH = DB_PATH
    todo_tools.DATABASE_PATH = DB_PATH
    
    init_conversation_tables()
    init_tool_call_tables()
    init_todo_tables()
    db_ready = True
except Exception as e:
    db_ready = False
    st.warning(f"⚠️ Database initialization: {str(e)}")

# Import agent components
AGENT_AVAILABLE = False
create_agent_func = None
get_mcp_tool_definitions_func = None
get_agent_config_func = None
store_message_func = None
MessageRole_enum = None
todo_tools_dict = {}

try:
    from phase_iii.agent import create_agent, get_mcp_tool_definitions
    from phase_iii.agent.config.agent_config import get_agent_config
    create_agent_func = create_agent
    get_mcp_tool_definitions_func = get_mcp_tool_definitions
    get_agent_config_func = get_agent_config
    AGENT_AVAILABLE = True
except Exception as e:
    st.error(f"❌ Failed to load agent: {str(e)}")

try:
    from phase_iii.persistence.repositories.conversation_repo import store_message
    from phase_iii.persistence.models.conversation import MessageRole
    store_message_func = store_message
    MessageRole_enum = MessageRole
except Exception as e:
    pass  # Optional - app works without persistence

try:
    from phase_iii.mcp_server.tools.todo_tools import (
        create_todo_tool, list_todos_tool, update_todo_tool,
        delete_todo_tool, get_todo_tool
    )
    todo_tools_dict = {
        "create_todo": create_todo_tool,
        "list_todos": list_todos_tool,
        "update_todo": update_todo_tool,
        "delete_todo": delete_todo_tool,
        "get_todo": get_todo_tool,
    }
except Exception as e:
    st.error(f"❌ Failed to load todo tools: {str(e)}")


def process_message(user_message: str):
    """Process user message and return agent response."""
    if not AGENT_AVAILABLE:
        return {
            "response_text": "I'm having trouble connecting. Please refresh the page and try again.",
            "tool_calls": [],
            "requires_tool_execution": False
        }
    
    try:
        # Always use MockProvider (no API key needed)
        agent = create_agent_func(api_key="mock", config=get_agent_config_func())
        tools = get_mcp_tool_definitions_func()
        
        # Get conversation history
        history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.conversation_history[-10:]
        ]
        
        # Process message
        agent_response = agent.process_message(
            user_message=user_message,
            conversation_history=history,
            user_id=st.session_state.user_id,
            tools=tools
        )
        
        # Execute tool calls if needed
        if agent_response.get("requires_tool_execution") and agent_response.get("tool_calls"):
            tool_results = []
            for tool_call in agent_response["tool_calls"]:
                tool_name = tool_call.get("name")
                tool_input = tool_call.get("input", {})
                
                if tool_name in todo_tools_dict and todo_tools_dict[tool_name]:
                    try:
                        result = todo_tools_dict[tool_name](**tool_input)
                        tool_results.append({
                            "tool_use_id": tool_call.get("tool_use_id", ""),
                            "result": result
                        })
                    except Exception as e:
                        tool_results.append({
                            "tool_use_id": tool_call.get("tool_use_id", ""),
                            "result": {"error": str(e)}
                        })
            
            # Process tool results
            if tool_results:
                try:
                    final_response = agent.process_tool_results(
                        tool_results=tool_results,
                        user_id=st.session_state.user_id
                    )
                    agent_response["response_text"] = final_response.get("response_text", agent_response.get("response_text", ""))
                except Exception as e:
                    pass  # Continue with original response
        
        return agent_response
        
    except Exception as e:
        return {
            "response_text": f"I'm sorry, I encountered an error: {str(e)}. Please try rephrasing your request.",
            "tool_calls": [],
            "requires_tool_execution": False
        }


# Main UI
st.title("✅ Todo Chat Assistant")
st.markdown("**Your friendly todo management assistant - No API key required!**")

# Welcome message for first-time users
if len(st.session_state.messages) == 0:
    st.info("👋 **Welcome!** I can help you manage your todos. Try saying things like:\n- \"Add task buy groceries\"\n- \"List my tasks\"\n- \"Mark task 1 as complete\"\n- \"Delete task 2\"")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.success("✅ **Mock Mode Active**\n\nNo API key needed! This app uses intelligent pattern matching to understand your commands.")
    
    st.markdown("---")
    st.markdown("### 📝 How to Use")
    st.markdown("""
    **Create Tasks:**
    - "Add task buy groceries"
    - "Create a task to call mom"
    - "Remind me to finish the report"
    
    **View Tasks:**
    - "List my tasks"
    - "Show all todos"
    - "What tasks do I have?"
    
    **Complete Tasks:**
    - "Mark task 1 as complete"
    - "ID 1 task completed"
    - "Task 2 is done"
    
    **Delete Tasks:**
    - "Delete task 1"
    - "Remove task 2"
    - "ID 3 delete"
    
    **Update Tasks:**
    - "Update task 1 to buy milk"
    - "Change task 2 to call dentist"
    """)
    
    st.markdown("---")
    st.markdown("### 🌍 Languages")
    st.markdown("Supports **English** and **Urdu (اردو)**")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation_history.append({"role": "user", "content": prompt})
    
    # Store user message (optional)
    if store_message_func and MessageRole_enum:
        try:
            store_message_func(
                user_id=st.session_state.user_id,
                role=MessageRole_enum.USER,
                content=prompt
            )
        except:
            pass  # Continue even if storage fails
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process message
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = process_message(prompt)
            
            response_text = response.get("response_text", "I'm sorry, I didn't understand that. Can you try rephrasing?")
            tool_calls = response.get("tool_calls", [])
            
            st.markdown(response_text)
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "tool_calls": tool_calls
    })
    st.session_state.conversation_history.append({"role": "assistant", "content": response_text})
    
    # Store assistant message (optional)
    if store_message_func and MessageRole_enum:
        try:
            store_message_func(
                user_id=st.session_state.user_id,
                role=MessageRole_enum.ASSISTANT,
                content=response_text
            )
        except:
            pass  # Continue even if storage fails

# Footer
st.markdown("---")
st.markdown("**Phase III - AI-Powered Todo Chat** | Built with Streamlit | Mock Mode - No API Key Required")
