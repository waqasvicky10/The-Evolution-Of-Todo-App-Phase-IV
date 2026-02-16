import sys
import os
from pathlib import Path

# Add project paths
PROJECT_ROOT = Path("e:/heckathon-2")
PHASE_III_PATH = PROJECT_ROOT / "phase_iii"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PHASE_III_PATH))

from dotenv import load_dotenv
load_dotenv("e:/heckathon-2/backend/.env", override=True)
os.environ["AI_MODEL"] = "qwen"
if not os.environ.get("QWEN_API_KEY"):
    os.environ["QWEN_API_KEY"] = "sk-dummy-key-for-test"

from agent import create_agent
print("Attempting to create agent...")
agent = create_agent()
print(f"Agent created successfully: {type(agent.provider).__name__}")
if hasattr(agent.provider, 'model'):
    print(f"Model: {agent.provider.model}")
