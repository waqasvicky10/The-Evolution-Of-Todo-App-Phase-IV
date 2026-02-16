# Todo App Backend

## Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server
```bash
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

The server will start at `http://localhost:8000`.
API Docs: `http://localhost:8000/docs`
