"""Test environment variable loading for Phase III"""
import os

# Try to load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env file loaded successfully")
except ImportError:
    print("⚠️  python-dotenv not installed, using system env vars")

# Check for API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    masked_key = api_key[:10] + "..." if len(api_key) > 10 else "***"
    print(f"✅ OPENAI_API_KEY found: {masked_key}")
else:
    print("⚠️  OPENAI_API_KEY not set - will use MockProvider")

# Check other vars
print(f"AGENT_MODEL: {os.getenv('AGENT_MODEL', 'not set (using default: gpt-4o-mini)')}")
print(f"AGENT_TEMPERATURE: {os.getenv('AGENT_TEMPERATURE', 'not set (using default: 0.7)')}")
print(f"AGENT_MAX_TOKENS: {os.getenv('AGENT_MAX_TOKENS', 'not set (using default: 4096)')}")
print(f"AGENT_TIMEOUT: {os.getenv('AGENT_TIMEOUT', 'not set (using default: 30)')}")
