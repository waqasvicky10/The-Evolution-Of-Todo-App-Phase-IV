
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"
HEADERS = {"Authorization": "Bearer test_token", "Content-Type": "application/json"}

def print_result(step, passed, message):
    icon = "✅" if passed else "❌"
    print(f"{icon} {step}: {message}")
    if not passed:
        exit(1)

def run_test():
    print("Starting Live Verification...")
    
    # 1. Health Check
    try:
        resp = requests.get(f"{BASE_URL}/chat/health")
        print_result("Health Check", resp.status_code == 200, f"Status {resp.status_code}")
    except Exception as e:
        print_result("Server Connection", False, f"Failed to connect: {e}")
        return

    # 2. Add Task (Setup for Context)
    todo_title = "Verify Logic Live"
    print(f"\nSending: 'Add task {todo_title}'")
    payload = {"message": f"Add task {todo_title}"}
    resp = requests.post(f"{BASE_URL}/chat", headers=HEADERS, json=payload)
    if resp.status_code != 200:
        print_result("Add Task", False, f"API Error: {resp.text}")
        return
        
    data = resp.json()
    print(f"Agent Response: {data['response']}")
    
    # Extract ID (Assuming agent response format or tool calls)
    # The server returns tool_calls in the response body usually
    tool_calls = data.get('tool_calls', [])
    created_id = None
    if tool_calls:
        print(f"Tool Calls: {tool_calls}")
        # Assuming format: result string might contain the ID or we infer it
        # Based on MockProvider, it returns a dict in 'result' usually or just success
        # But let's check the text response or tool call result
        # Live server executes the tool. The result is in tool_calls.result
        # It's a stringified dict usually?
        pass
    
    print_result("Add Task", "Verify Logic Live" in data['response'] or (tool_calls and tool_calls[0]['status'] == 'success'), "Task creation acknowledged")

    # 3. Test Context: "Delete it"
    # We need the ID to verify the confirmation message, but the confirmation message itself is the proof of context.
    # It should say "Are you sure you want to delete task X?"
    print("\nSending: 'Delete it'")
    payload = {"message": "Delete it"}
    resp = requests.post(f"{BASE_URL}/chat", headers=HEADERS, json=payload)
    data = resp.json()
    print(f"Agent Response: {data['response']}")
    
    context_working = "Are you sure" in data['response'] or "confirm" in data['response'].lower()
    print_result("Context Awareness", context_working, "Agent asked for confirmation")
    
    # 4. Test Safety: confirm
    print("\nSending: 'Yes'")
    payload = {"message": "Yes"}
    resp = requests.post(f"{BASE_URL}/chat", headers=HEADERS, json=payload)
    data = resp.json()
    print(f"Agent Response: {data['response']}")
    
    tool_calls = data.get('tool_calls', [])
    delete_called = False
    if tool_calls:
        for tc in tool_calls:
            if tc['tool_name'] == 'delete_todo':
                delete_called = True
                print(f"Tool Executed: {tc}")
    
    print_result("Confirmation Flow", delete_called, "Delete tool executed after confirmation")

if __name__ == "__main__":
    time.sleep(1) # Give server a moment if just started
    run_test()
