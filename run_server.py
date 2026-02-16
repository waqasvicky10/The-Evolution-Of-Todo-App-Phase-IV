import asyncio
from uvicorn import Config, Server
import os
import sys
sys.path.insert(0, os.getcwd())

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Import the app
from phase_iii.main import app

async def run_server():
    config = Config(app=app, host="127.0.0.1", port=9000, log_level="info")
    server = Server(config)
    await server.serve()

if __name__ == "__main__":
    print("Starting server...")
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("Server stopped.")
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()