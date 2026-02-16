import os
import sys
from pathlib import Path

# Add phase_iii to path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
PHASE_III_PATH = PROJECT_ROOT / "phase_iii"
sys.path.insert(0, str(PHASE_III_PATH))
sys.path.insert(0, str(PROJECT_ROOT))

print(f"Script directory: {SCRIPT_DIR}")
print(f"Project root: {PROJECT_ROOT}")
print(f"Phase III path: {PHASE_III_PATH}")
print()

# Try loading dotenv
try:
    from dotenv import load_dotenv
    print("Testing dotenv loading...")
    
    # Test 1: Load from current directory
    print(f"\n1. Current working directory: {os.getcwd()}")
    load_dotenv(override=True)
    print(f"   AI_MODEL from env: {os.getenv('AI_MODEL', 'NOT SET')}")
    
    # Test 2: Load from project root
    root_env = PROJECT_ROOT / ".env"
    print(f"\n2. Loading from project root: {root_env}")
    load_dotenv(root_env, override=True)
    print(f"   AI_MODEL from env: {os.getenv('AI_MODEL', 'NOT SET')}")
    
    # Test 3: Load from backend
    backend_env = PROJECT_ROOT / "backend" / ".env"
    print(f"\n3. Loading from backend: {backend_env}")
    load_dotenv(backend_env, override=True)
    print(f"   AI_MODEL from env: {os.getenv('AI_MODEL', 'NOT SET')}")
    
except ImportError as e:
    print(f"dotenv not available: {e}")

print("\n" + "="*50)
print("Now testing agent creation...")
print("="*50 + "\n")

try:
    from agent import create_agent
    from agent.config.agent_config import get_agent_config
    
    agent = create_agent(api_key="mock", config=get_agent_config())
    print(f"Agent created successfully!")
    print(f"Provider type: {type(agent.provider).__name__}")
    print(f"Model info: {agent.get_model_info()}")
except Exception as e:
    print(f"Error creating agent: {e}")
    import traceback
    traceback.print_exc()
