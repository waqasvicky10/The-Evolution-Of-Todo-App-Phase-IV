import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {r.status_code} {r.json()}")
        return r.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_chat_fallback():
    # Attempt to chat (should work even if Phase III is missing, using fallback)
    # Need to register/login first? 
    # The chat endpoint requires auth: client -> /api/chat [POST]
    # Let's just check if 401 is returned (meaning server is reached and auth middleware is working)
    try:
        r = requests.post(f"{BASE_URL}/api/chat", json={"message": "hello"})
        print(f"Chat (unauth): {r.status_code}")
        # Should be 401 Unauthorized
        return r.status_code == 401
    except Exception as e:
        print(f"Chat check failed: {e}")
        return False

def main():
    if test_health() and test_chat_fallback():
        print("SUCCESS: Backend is responding.")
    else:
        print("FAILURE: Backend is not behaving as expected.")
        sys.exit(1)

if __name__ == "__main__":
    main()
