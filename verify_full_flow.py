import requests
import os
from dotenv import load_dotenv
import time

load_dotenv("e:/heckathon-2/backend/.env", override=True)

BASE_URL = "http://localhost:8000/api"
EMAIL = f"test_{int(time.time())}@example.com"
PASSWORD = "Password123!"

def verify_flow():
    try:
        # 1. Register
        print(f"Registering user: {EMAIL}")
        reg_res = requests.post(f"{BASE_URL}/auth/register", json={
            "email": EMAIL,
            "password": PASSWORD,
            "password_confirmation": PASSWORD
        })
        print(f"Register status: {reg_res.status_code}")
        
        # 2. Login
        print("Logging in...")
        login_res = requests.post(f"{BASE_URL}/auth/login", json={
            "email": EMAIL,
            "password": PASSWORD
        })
        print(f"Login status: {login_res.status_code}")
        if login_res.status_code != 200:
            print(f"Login failed: {login_res.text}")
            return
            
        token = login_res.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Get Chat History
        print("Fetching chat history...")
        hist_res = requests.get(f"{BASE_URL}/chat/history", headers=headers)
        print(f"History status: {hist_res.status_code}")
        if hist_res.status_code == 200:
            print("Chat history retrieved SUCCESSFULLY!")
            print(f"Messages: {len(hist_res.json().get('messages', []))}")
        else:
            print(f"History failed with {hist_res.status_code}: {hist_res.text}")
            
    except Exception as e:
        print(f"Error during verification: {e}")

if __name__ == "__main__":
    verify_flow()
