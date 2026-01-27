"""
Test script to verify Phase III agent imports work correctly.
Run this from the backend directory to diagnose import issues.
"""

import sys
from pathlib import Path

# Calculate paths
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
PHASE_III_PATH = PROJECT_ROOT / "phase_iii"

print(f"Backend dir: {BACKEND_DIR}")
print(f"Project root: {PROJECT_ROOT}")
print(f"Phase III path: {PHASE_III_PATH}")
print(f"Phase III exists: {PHASE_III_PATH.exists()}")

# Add to path
if str(PHASE_III_PATH) not in sys.path:
    sys.path.insert(0, str(PHASE_III_PATH))
    print(f"Added to sys.path: {PHASE_III_PATH}")

# Try imports
try:
    print("\n--- Testing imports ---")
    from agent import create_agent, get_mcp_tool_definitions
    print("✅ agent imported")
    
    from agent.config.agent_config import get_agent_config
    print("✅ agent_config imported")
    
    from mcp_server.tools.todo_tools import (
        create_todo_tool,
        list_todos_tool,
        update_todo_tool,
        delete_todo_tool,
        get_todo_tool
    )
    print("✅ todo_tools imported")
    
    # Test agent creation
    print("\n--- Testing agent creation ---")
    config = get_agent_config()
    print(f"✅ Config loaded: {type(config)}")
    
    agent = create_agent(api_key="mock", config=config)
    print(f"✅ Agent created: {type(agent)}")
    
    tools = get_mcp_tool_definitions()
    print(f"✅ Tools loaded: {len(tools)} tools")
    
    # Test message processing
    print("\n--- Testing message processing ---")
    test_message = "Add a task to buy groceries"
    history = []
    
    response = agent.process_message(
        user_message=test_message,
        conversation_history=history,
        user_id=1,
        tools=tools
    )
    
    print(f"✅ Response received: {type(response)}")
    print(f"Response keys: {response.keys() if isinstance(response, dict) else 'Not a dict'}")
    print(f"Response text: {response.get('response_text', 'No response_text')[:100]}")
    print(f"Requires tool execution: {response.get('requires_tool_execution', False)}")
    
    print("\n✅ All tests passed! Phase III agent is working correctly.")
    
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
