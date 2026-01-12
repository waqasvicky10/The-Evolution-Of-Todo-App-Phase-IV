
import asyncio
import os
from unittest.mock import MagicMock
from phase_iii.chat_api.routes.chat import chat
from phase_iii.chat_api.schemas.chat_schemas import ChatMessageRequest

# Set dummy API key for test if not present
if "ANTHROPIC_API_KEY" not in os.environ:
    os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test"

async def test_chat_flow():
    print("Starting integration test for Chat API...")
    
    # Mock message request
    request = ChatMessageRequest(message="Add a task to test the chatbot")
    
    # Set user_id
    user_id = 1
    
    try:
        # We need to make sure the database is initialized
        from phase_iii.persistence.repositories.conversation_repo import init_conversation_tables
        from phase_iii.persistence.repositories.tool_call_repo import init_tool_call_tables
        init_conversation_tables()
        init_tool_call_tables()
        
        print("Database initialized.")
        
        # Invoke chat endpoint logic
        # Note: This will actually call Anthropic if the key is real
        # For a pure dry run, we might need more mocking, 
        # but let's see if it gets through the logic.
        response = await chat(request, user_id=user_id)
        
        print("\n--- Agent Response ---")
        print(f"Response: {response.response}")
        print(f"Tool Calls: {len(response.tool_calls)}")
        for tc in response.tool_calls:
            print(f"  - Tool: {tc.tool_name}")
            print(f"    Params: {tc.parameters}")
            print(f"    Result: {tc.result}")
        print("----------------------\n")
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chat_flow())
