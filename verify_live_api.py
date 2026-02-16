import requests
import sys
import time
import json

BASE_URL = "http://localhost:8000"

print(f"Waiting for server at {BASE_URL}...")

max_retries = 10
for i in range(max_retries):
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("Server is UP!")
            break
    except requests.exceptions.ConnectionError:
        print(f"Waiting... ({i+1}/{max_retries})")
        time.sleep(2)
else:
    print("Server failed to start.")
    sys.exit(1)

# Test Chat Endpoint
print("\nTesting Chat Endpoint...")
# Login first (mock login or get token if needed, but chat might be protected)
# Check chat.py: router = APIRouter(prefix="/api/chat", tags=["Chat"])
# It uses Depends(get_current_user). We need a token.

# Let's try to register/login first
email = "test@example.com"
password = "password123"

# Register
try:
    print("Registering test user...")
    requests.post(f"{BASE_URL}/api/v1/auth/signup", json={
        "email": email,
        "password": password,
        "full_name": "Test User"
    })
except:
    pass # Might already exist

# Login
print("Logging in...")
try:
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", data={
        "username": email,
        "password": password
    })
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        # Try default user
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", data={
            "username": "user@example.com",
            "password": "password"
        })
        if response.status_code != 200:
            print("Default login failed too.")
            sys.exit(1)

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful.")

    # Send Chat Message
    print("\nSending 'Hello' to chat...")
    chat_response = requests.post(
        f"{BASE_URL}/api/chat",
        headers=headers,
        json={"message": "Hello, are you working?"}
    )
    
    print(f"Status: {chat_response.status_code}")
    try:
        data = chat_response.json()
        print(json.dumps(data, indent=2))
        
        response_text = data.get("response")
        if "encountered an error" in response_text and "Error code" not in response_text:
             print("\n❌ FAILURE: Still seeing generic error message.")
        elif "encountered an error" in response_text:
             print("\n✅ PARTIAL SUCCESS: Seeing DETAILED error message (Good!)")
        else:
             print("\n✅ SUCCESS: Agent responded normally.")

    except Exception as e:
        print(f"Failed to parse response: {chat_response.text}")

except Exception as e:
    print(f"Test failed: {e}")
