import sys
import os

try:
    from openai import OpenAI
    print(f"OpenAI package imported successfully. Version: {getattr(__import__('openai'), '__version__', 'unknown')}")
except ImportError:
    print("Failed to import openai")
    sys.exit(1)

try:
    api_key = os.getenv("OPENAI_API_KEY", "sk-test-key")
    print(f"Attempting to initialize OpenAI client with key: {api_key[:10]}...")
    client = OpenAI(api_key=api_key)
    print("OpenAI client initialized successfully!")
except Exception as e:
    print(f"Failed to initialize OpenAI client: {e}")
    import traceback
    traceback.print_exc()
