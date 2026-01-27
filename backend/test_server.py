"""Quick test script to verify server is running."""
import requests

try:
    print("Testing server at http://127.0.0.1:8000...")
    response = requests.get("http://127.0.0.1:8000/health", timeout=5)
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Response: {response.json()}")
    print("\n✅ Server is working!")
    
    # Test root endpoint
    print("\nTesting root endpoint...")
    response = requests.get("http://127.0.0.1:8000/", timeout=5)
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Response: {response.json()}")
    
except requests.exceptions.ConnectionError:
    print("❌ Server is not running or not accessible")
    print("   Make sure you started the server with: uvicorn app.main:app --reload")
except requests.exceptions.Timeout:
    print("❌ Server is not responding (timeout)")
except Exception as e:
    print(f"❌ Error: {e}")
