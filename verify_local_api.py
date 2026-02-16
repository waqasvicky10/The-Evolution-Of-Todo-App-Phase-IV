import requests
import os
from dotenv import load_dotenv

load_dotenv("e:/heckathon-2/backend/.env", override=True)

BASE_URL = "http://localhost:8000/api"

def test_health():
    try:
        # Check if backend is alive
        # Note: There might not be a dedicated /health, so we try /auth/login with bad creds 
        # just to see if we get a response (401 is better than "Connection Refused")
        response = requests.post(f"{BASE_URL}/auth/login", json={"email": "test@example.com", "password": "wrong"})
        print(f"Backend Response Code: {response.status_code}")
        print(f"Backend Response Body: {response.json()}")
    except Exception as e:
        print(f"Error connecting to backend: {e}")

if __name__ == "__main__":
    print(f"Testing local backend at {BASE_URL}")
    print(f"SECRET_KEY in env: {os.getenv('SECRET_KEY')}")
    print(f"AI_MODEL in env: {os.getenv('AI_MODEL')}")
    test_health()
