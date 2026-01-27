"""
Diagnostic script to test chat endpoint and see exact errors.
Run this to see what's failing.
"""

import sys
from pathlib import Path

# Add paths
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
PHASE_III_PATH = PROJECT_ROOT / "phase_iii"

sys.path.insert(0, str(PHASE_III_PATH))

print("=" * 60)
print("DIAGNOSING CHAT API ERRORS")
print("=" * 60)

# Test 1: Import Phase III components
print("\n1. Testing Phase III imports...")
try:
    from agent import create_agent, get_mcp_tool_definitions
    from agent.config.agent_config import get_agent_config
    print("   ✅ Imports successful")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Create agent
print("\n2. Testing agent creation...")
try:
    agent = create_agent(api_key="mock", config=get_agent_config())
    print(f"   ✅ Agent created: {type(agent)}")
except Exception as e:
    print(f"   ❌ Agent creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Get tools
print("\n3. Testing tool definitions...")
try:
    tools = get_mcp_tool_definitions()
    print(f"   ✅ Tools loaded: {len(tools)} tools")
    for tool in tools:
        print(f"      - {tool.get('name', 'unknown')}")
except Exception as e:
    print(f"   ❌ Tool loading failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Process a message
print("\n4. Testing message processing...")
try:
    test_message = "Add a task to buy groceries"
    history = []
    
    response = agent.process_message(
        user_message=test_message,
        conversation_history=history,
        user_id=1,
        tools=tools
    )
    
    print(f"   ✅ Response received")
    print(f"      Keys: {list(response.keys())}")
    print(f"      Requires tool execution: {response.get('requires_tool_execution', False)}")
    print(f"      Response text: {response.get('response_text', 'N/A')[:100]}")
    
    if response.get("tool_calls"):
        print(f"      Tool calls: {len(response['tool_calls'])}")
        for tc in response["tool_calls"]:
            print(f"         - {tc.get('name', 'unknown')}: {tc.get('input', {})}")
    
except Exception as e:
    print(f"   ❌ Message processing failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Test tool results format
print("\n5. Testing tool results processing...")
try:
    # Simulate tool results
    test_tool_results = [
        {
            "content": {
                "success": True,
                "todo_id": 1,
                "title": "Test task",
                "completed": False
            }
        }
    ]
    
    final_response = agent.process_tool_results(
        tool_results=test_tool_results,
        user_id=1
    )
    
    print(f"   ✅ Tool results processed")
    print(f"      Final response: {final_response.get('response_text', 'N/A')[:100]}")
    
except Exception as e:
    print(f"   ❌ Tool results processing failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - Phase III components working correctly!")
print("=" * 60)
print("\nIf chat still fails, the issue is in the FastAPI integration.")
print("Check backend logs when you send a chat message.")
