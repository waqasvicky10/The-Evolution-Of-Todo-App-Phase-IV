# Todo Chat UI

A simple, modern chat interface for the AI-Powered Todo Chatbot.

## Features

- 💬 Real-time chat with AI assistant
- 📝 Conversation history persistence
- 🔐 Authentication support
- 📱 Responsive design
- 🎨 Clean, modern UI

## Setup

### Prerequisites

1. FastAPI backend running on `http://localhost:8000`
2. Environment variable `ANTHROPIC_API_KEY` set with your Anthropic API key

### Running the UI

#### Option 1: Using Python's built-in HTTP server

```bash
cd phase_iii/chat_ui
python -m http.server 8080
```

Then open your browser to: `http://localhost:8080`

#### Option 2: Using Node.js http-server

```bash
cd phase_iii/chat_ui
npx http-server -p 8080
```

Then open your browser to: `http://localhost:8080`

#### Option 3: Open directly in browser

Simply open `index.html` in your web browser. Note: You may need to enable CORS in your browser or configure the FastAPI backend to allow CORS from `file://` origins.

## Usage

### 1. Start the Backend

First, start the FastAPI chat API server:

```bash
cd phase_iii
python -m uvicorn chat_api.main:app --reload --host 0.0.0.0 --port 8000
```

Or:

```bash
cd phase_iii
python chat_api/main.py
```

### 2. Login

- Username: any (for demo)
- Password: any (for demo)

The demo uses a test token (`test_token`) for authentication.

### 3. Start Chatting!

Try these example commands:

- "Add a task to buy groceries"
- "Show me my tasks"
- "Mark the grocery task as done"
- "Delete the grocery task"
- "Create a todo to call mom tomorrow"
- "List all my incomplete tasks"

## Configuration

### API Endpoint

To change the API endpoint, edit `chat.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

### Authentication

Currently uses a test token for demo purposes. To implement real authentication:

1. Create a login endpoint in FastAPI that returns a JWT token
2. Update `handleLogin()` in `chat.js` to call the authentication endpoint
3. Update `get_current_user_id()` in `chat_api/routes/chat.py` to properly decode JWT tokens

## File Structure

```
chat_ui/
├── index.html      # Main HTML structure
├── styles.css      # UI styling
├── chat.js         # JavaScript logic
└── README.md       # This file
```

## Features Implemented

### ✅ Message Display
- User and assistant message bubbles
- Message timestamps
- Tool call indicators
- Auto-scroll to latest message

### ✅ User Input Handling
- Message input field
- Send button with loading state
- Enter key to send
- Input validation

### ✅ Conversation History Loading
- Loads previous messages on login
- Displays in chronological order
- Persists across sessions

### ✅ Authentication Context
- Login/logout functionality
- Token storage in localStorage
- Session persistence
- User name display

### ✅ Error Handling
- Network error handling
- Session expiration handling
- User-friendly error messages
- Error toast notifications

## Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Responsive design

## Troubleshooting

### CORS Errors

If you see CORS errors in the browser console, make sure the FastAPI backend has CORS configured properly:

```python
# In chat_api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection Failed

1. Check that the FastAPI server is running: `curl http://localhost:8000/health`
2. Verify the API_BASE_URL in `chat.js` matches your server
3. Check browser console for detailed error messages

### Messages Not Loading

1. Verify authentication token is valid
2. Check that the database has conversation history
3. Open browser DevTools Network tab to see API responses

## Production Deployment

For production use:

1. **Implement real authentication**
   - Use JWT tokens
   - Secure token storage
   - Token refresh mechanism

2. **Enable HTTPS**
   - Use SSL certificates
   - Update API_BASE_URL to use `https://`

3. **Configure CORS properly**
   - Whitelist specific origins
   - Remove wildcard (`*`) origins

4. **Add error tracking**
   - Integrate with error monitoring service
   - Log client-side errors

5. **Optimize assets**
   - Minify JavaScript and CSS
   - Enable caching
   - Use a CDN

## Future Enhancements

- [ ] Markdown support in messages
- [ ] File upload capability
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Message search
- [ ] Export conversation history
- [ ] Typing indicators
- [ ] Read receipts

## License

Part of "The Evolution of Todo App" - Phase III
