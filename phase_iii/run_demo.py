import requests
import json
import time

BASE_URL = "http://localhost:8000/api/chat"
HEADERS = {
    "Authorization": "Bearer test_token",
    "Content-Type": "application/json"
}

def send_message(message, label):
    print(f"\n[{label}] Sending: '{message}'")
    try:
        response = requests.post(BASE_URL, headers=HEADERS, json={"message": message})
        if response.status_code == 200:
            data = response.json()
            print(f"🤖 Agent: {data['response']}")
            if data.get('tool_calls'):
                for tool in data['tool_calls']:
                    print(f"   🛠️ Tool Executed: {tool['tool_name']} -> Status: {tool['status']}")
            return data
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def run_demo():
    print("🚀 Starting Automated Todo App Demo...")
    print("=======================================")
    
    # 2. Add English Task
    resp = send_message("Add a task to buy fresh milk", "1. Create (English)")
    id1 = None
    if resp and resp.get('tool_calls'):
        # Extract ID from result string or tool result if accessible. 
        # The agent response text usually contains the ID or we can parse the tool result if we had it structured.
        # But here valid JSON is in 'tool_calls' -> 'result' but our API schema wraps it.
        # Let's just Regex the response text for "ID: <num>"
        import re
        match = re.search(r"ID:\s*(\d+)", resp['response'])
        if match:
            id1 = match.group(1)
            print(f"   ℹ️ Captured ID: {id1}")
    time.sleep(1)
    
    # 3. Add Urdu Task
    resp = send_message("کتاب پڑھنا شامل کریں", "2. Create (Urdu)")
    id2 = None
    if resp:
         match = re.search(r"ID:?\s*(\d+)", resp['response']) # Urdu response might vary slightly
         if match:
            id2 = match.group(1)
            print(f"   ℹ️ Captured ID: {id2}")
    time.sleep(1)
    
    # 4. List Tasks
    send_message("Show my todo list", "3. List Todos")
    time.sleep(1)
    
    # 5. Complete Task
    if id1:
        send_message(f"Mark task {id1} as done", f"4. Complete Task {id1}")
    else:
        print("⚠️ Could not capture ID for completion, trying 1...")
        send_message("Mark task 1 as done", "4. Complete Task 1")
    time.sleep(1)
    
    # 6. Verify Completion
    send_message("Show my list", "5. Verify List")
    time.sleep(1)
    
    # 7. Delete Task
    if id1:
        send_message(f"Delete task {id1}", f"6. Delete Task {id1}")
    time.sleep(1)
    
    # 8. Final List
    send_message("فہرست دکھائیں", "7. Final List (Urdu)")
    
    print("\n=======================================")
    print("✅ Demo Complete!")

if __name__ == "__main__":
    run_demo()
