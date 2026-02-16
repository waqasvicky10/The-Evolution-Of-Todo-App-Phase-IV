import requests
import json

base_url = "http://localhost:8000/api"

def test_auth():
    # 1. Register
    reg_data = {
        "email": "test_bot@example.com",
        "password": "Password123!",
        "password_confirmation": "Password123!"
    }
    print(f"Testing registration for {reg_data['email']}...")
    res = requests.post(f"{base_url}/auth/register", json=reg_data)
    print(f"Register status: {res.status_code}")
    print(f"Register response: {res.text}")

    if res.status_code in [201, 409]:
        # 2. Login
        login_data = {
            "email": reg_data["email"],
            "password": reg_data["password"]
        }
        print(f"Testing login for {login_data['email']}...")
        res = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login status: {res.status_code}")
        print(f"Login response: {res.text}")
        
        if res.status_code == 200:
            token = res.json()["access_token"]
            # 3. Test protected route
            print("Testing protected route /api/tasks...")
            headers = {"Authorization": f"Bearer {token}"}
            res = requests.get(f"{base_url}/tasks", headers=headers)
            print(f"Tasks status: {res.status_code}")
            print(f"Tasks response: {res.text}")

if __name__ == "__main__":
    test_auth()
