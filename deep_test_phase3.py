
import os
import asyncio
import json
from phase_iii.persistence.repositories.conversation_repo import init_conversation_tables, store_message
from phase_iii.persistence.repositories.tool_call_repo import init_tool_call_tables
from phase_iii.mcp_server.tools.todo_tools import init_todo_tables
from phase_iii.chat_api.routes.chat import chat
from phase_iii.chat_api.schemas.chat_schemas import ChatMessageRequest

async def test_e2e_flow():
    print("🚀 Starting Phase III Deep Test...")
    
    # 1. Environment Check
    print(f"Current Directory: {os.getcwd()}")
    
    # 2. Initialize Tables
    print("Initialize Tables...")
    try:
        init_conversation_tables()
        init_tool_call_tables()
        init_todo_tables()
        print("✅ Tables Initialized Successfully.")
    except Exception as e:
        print(f"❌ Table Initialization Failed: {e}")
        return

    # 3. Test Chat API (Implicit Add)
    print("\nTesting 'a task by milk'...")
    try:
        request = ChatMessageRequest(message="a task by milk")
        # In a real API call, Depends(get_current_user_id) would run. 
        # Here we 'mock' the dependency by passing the result if we were calling the function, 
        # but chat() expects user_id as a parameter if called directly.
        
        response = await chat(request, user_id=1)
        
        print(f"Response: {response.response}")
        print(f"Tool Calls: {len(response.tool_calls)}")
        
        assert "milk" in response.response.lower()
        assert len(response.tool_calls) > 0
        assert response.tool_calls[0].tool_name == "create_todo"
        print("✅ Implicit Add Test Passed.")
    except Exception as e:
        print(f"❌ Implicit Add Test Failed: {e}")
        import traceback
        traceback.print_exc()

    # 4. Test Chat API (List)
    print("\nTesting 'show my list'...")
    try:
        request = ChatMessageRequest(message="show my list")
        response = await chat(request, user_id=1)
        
        print(f"Response Content: {response.response}")
        assert "milk" in response.response.lower()
        print("✅ List Test Passed.")
    except Exception as e:
        print(f"❌ List Test Failed: {e}")

    # 5. Test Urdu
    print("\nTesting Urdu: 'ایک کام شامل کریں دودھ خریدنا'...")
    try:
        request = ChatMessageRequest(message="ایک کام شامل کریں دودھ خریدنا")
        response = await chat(request, user_id=1)
        print(f"Response: {response.response}")
        # Check if the title was captured correctly (should contain 'خریدنا')
        if "خریدنا" in response.response or "ایک کام" in response.response:
             print("✅ Urdu Test Passed (Captured title).")
        else:
             print("❌ Urdu Test Failed (Title not captured correctly).")
             return False
    except Exception as e:
        print(f"❌ Urdu Test Failed: {e}")
        return False

    return True

async def main():
    success = await test_e2e_flow()
    if success:
        print("\n🎉 PHASE III DEEP TEST: PASSED")
        sys.exit(0)
    else:
        print("\n❌ PHASE III DEEP TEST: FAILED")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure we run in the right context
    import sys
    # Add project root to sys.path
    project_root = os.getcwd()
    if project_root not in sys.path:
        sys.path.append(project_root)
        
    asyncio.run(main())
