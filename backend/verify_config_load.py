import os
import sys

# Add the current directory to the python path so imports work
sys.path.append(os.getcwd())

from app.config import settings

def main():
    print("Checking loaded configuration...")
    key = settings.OPENAI_API_KEY
    if not key:
        print("  OPENAI_API_KEY not loaded!")
    else:
        masked = key[:5] + "..." + key[-4:] if len(key) > 10 else "Too short"
        print(f"  Loaded OPENAI_API_KEY: {masked}")
        
    print(f"  Environment: {settings.ENVIRONMENT}")

if __name__ == "__main__":
    main()
