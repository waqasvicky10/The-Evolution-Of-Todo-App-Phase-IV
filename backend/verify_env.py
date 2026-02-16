import os
from dotenv import load_dotenv

def check_env_file(path, name):
    print(f"Checking {name} at {path}...")
    if not os.path.exists(path):
        print(f"  File not found: {path}")
        return
    
    # Read manually to avoid polluting environment
    with open(path, 'r') as f:
        content = f.read()
        
    for line in content.splitlines():
        if line.startswith("OPENAI_API_KEY="):
            key = line.split("=", 1)[1].strip()
            masked = key[:5] + "..." + key[-4:] if len(key) > 10 else "Too short"
            print(f"  OPENAI_API_KEY found: {masked}")
            return
            
    print("  OPENAI_API_KEY not found in file")

def main():
    print("Current working directory:", os.getcwd())
    check_env_file(".env", "Backend .env")
    check_env_file("../.env", "Root .env")

if __name__ == "__main__":
    main()
