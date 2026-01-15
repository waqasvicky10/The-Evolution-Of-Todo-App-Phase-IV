"""
Phase III Todo Chat App - Streamlit Deployment
AI-Powered Todo Assistant with Voice Support

This is the main entry point for Streamlit Cloud deployment.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add phase_iii to path so imports work
project_root = Path(__file__).parent
phase_iii_path = project_root / "phase_iii"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(phase_iii_path))

# Page configuration
st.set_page_config(
    page_title="Todo Chat - AI Assistant",
    page_icon="🤖",
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

# Initialize database tables
try:
    from phase_iii.persistence.repositories.conversation_repo import init_conversation_tables
    from phase_iii.persistence.repositories.tool_call_repo import init_tool_call_tables
    from phase_iii.mcp_server.tools.todo_tools import init_todo_tables
    
    init_conversation_tables()
    init_tool_call_tables()
    init_todo_tables()
except Exception as e:
    st.warning(f"Database initialization: {e}")

# Import agent
try:
    from phase_iii.agent import create_agent, get_mcp_tool_definitions
    from phase_iii.agent.config.agent_config import get_agent_config
    from phase_iii.persistence.repositories.conversation_repo import (
        store_message, get_recent_messages
    )
    from phase_iii.persistence.models.conversation import MessageRole
    from phase_iii.mcp_server.tools.todo_tools import (
        create_todo_tool, list_todos_tool, update_todo_tool,
        delete_todo_tool, get_todo_tool
    )
    
    AGENT_AVAILABLE = True
except Exception as e:
    st.error(f"Failed to import agent modules: {e}")
    import traceback
    st.code(traceback.format_exc())
    AGENT_AVAILABLE = False

# Tool mapping
TOOL_MAP = {
    "create_todo": create_todo_tool if AGENT_AVAILABLE else None,
    "list_todos": list_todos_tool if AGENT_AVAILABLE else None,
    "update_todo": update_todo_tool if AGENT_AVAILABLE else None,
    "delete_todo": delete_todo_tool if AGENT_AVAILABLE else None,
    "get_todo": get_todo_tool if AGENT_AVAILABLE else None,
}


def process_message(user_message: str):
    """Process user message and return agent response."""
    if not AGENT_AVAILABLE:
        return {
            "response_text": "Agent is not available. Please check the logs.",
            "tool_calls": [],
            "requires_tool_execution": False
        }
    
    try:
        # Get API key from environment (set by sidebar)
        api_key = os.getenv("OPENAI_API_KEY", "")
        
        # Get agent (will use OpenAI if API key is set, otherwise MockProvider)
        agent = create_agent(api_key=api_key if api_key else "mock", config=get_agent_config())
        tools = get_mcp_tool_definitions()
        
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
                
                if tool_name in TOOL_MAP and TOOL_MAP[tool_name]:
                    try:
                        result = TOOL_MAP[tool_name](**tool_input)
                        tool_results.append({
                            "tool_use_id": tool_call.get("tool_use_id", ""),
                            "result": result
                        })
                    except Exception as e:
                        tool_results.append({
                            "tool_use_id": tool_call.get("tool_use_id", ""),
                            "result": {"error": str(e)}
                        })
            
            # Process tool results (agent.process_tool_results requires user_id)
            if tool_results:
                try:
                    final_response = agent.process_tool_results(
                        tool_results=tool_results,
                        user_id=st.session_state.user_id
                    )
                    agent_response["response_text"] = final_response.get("response_text", agent_response.get("response_text", ""))
                except Exception as e:
                    st.warning(f"Tool result processing: {e}")
        
        return agent_response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        st.error(f"Error details: {error_details}")
        return {
            "response_text": f"I'm sorry, I encountered an error: {str(e)}. Please check the error details above or try again.",
            "tool_calls": [],
            "requires_tool_execution": False
        }


# Main UI
st.title("🤖 Todo Chat - AI Assistant")
st.markdown("**Your AI-powered todo management assistant with voice support**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key input
    openai_key = st.text_input(
        "OpenAI API Key (Optional)",
        type="password",
        help="Leave empty to use MockProvider (limited functionality)"
    )
    
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
        st.success("✅ OpenAI API Key set")
    else:
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        st.info("ℹ️ Using MockProvider (no API key needed)")
    
    st.markdown("---")
    st.markdown("### 📝 Instructions")
    st.markdown("""
    **Voice Commands:**
    - "Add task buy groceries"
    - "List my tasks"
    - "ID 1 task completed"
    - "Delete task 2"
    
    **Supported Languages:**
    - English
    - Urdu (اردو)
    """)
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show tool calls if any
        if "tool_calls" in message and message["tool_calls"]:
            with st.expander("🔧 Tool Calls"):
                for tool_call in message["tool_calls"]:
                    st.json(tool_call)

# Chat input
if prompt := st.chat_input("Type your message or use voice commands..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation_history.append({"role": "user", "content": prompt})
    
    # Store user message
    try:
        if AGENT_AVAILABLE:
            store_message(
                user_id=st.session_state.user_id,
                role=MessageRole.USER,
                content=prompt
            )
    except Exception as e:
        st.warning(f"Failed to store message: {e}")
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process message
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = process_message(prompt)
                
                response_text = response.get("response_text", "I'm sorry, I didn't understand that.")
                tool_calls = response.get("tool_calls", [])
                
                # Check if response indicates an error
                if "error" in response_text.lower() or "sorry" in response_text.lower():
                    st.error("⚠️ " + response_text)
                else:
                    st.markdown(response_text)
                
                # Show tool calls
                if tool_calls:
                    with st.expander("🔧 Tool Calls Executed"):
                        for tool_call in tool_calls:
                            st.json(tool_call)
            except Exception as e:
                import traceback
                st.error(f"❌ Error: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.code(traceback.format_exc())
                response_text = f"I'm sorry, I encountered an error: {str(e)}"
                tool_calls = []
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "tool_calls": tool_calls
    })
    st.session_state.conversation_history.append({"role": "assistant", "content": response_text})
    
    # Store assistant message
    try:
        if AGENT_AVAILABLE:
            store_message(
                user_id=st.session_state.user_id,
                role=MessageRole.ASSISTANT,
                content=response_text
            )
    except Exception as e:
        st.warning(f"Failed to store response: {e}")

# Footer
st.markdown("---")
st.markdown("**Phase III - AI-Powered Todo Chat** | Built with Streamlit")
