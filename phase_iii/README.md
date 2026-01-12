# Phase III - AI-Powered Todo Chatbot

## Directory Structure

This directory contains all Phase III implementation code, clearly separated from Phase II code.

### Architecture Overview

```
phase_iii/
├── mcp_server/          # MCP Server (Tool Execution Layer)
├── agent/               # OpenAI Agent (AI Reasoning Layer)
├── chat_api/            # FastAPI Chat Endpoints (API Gateway)
├── persistence/         # Conversation & Tool Call Storage
└── tests/               # Phase III Tests
```

---

## Component Details

### 1. MCP Server (`mcp_server/`)

**Responsibility:** Expose todo operations as MCP tools and act as exclusive data gateway.

```
mcp_server/
├── __init__.py          # Package initialization
├── server.py            # MCP Server initialization and setup
├── tools/               # Tool implementations
│   ├── __init__.py
│   ├── create_todo.py   # Create todo tool
│   ├── list_todos.py    # List todos tool
│   ├── update_todo.py   # Update todo tool
│   ├── complete_todo.py # Complete todo tool
│   └── delete_todo.py   # Delete todo tool
├── schemas/             # Tool schemas and definitions
│   ├── __init__.py
│   ├── tool_schemas.py  # MCP tool schema definitions
│   └── responses.py     # Tool response formats
└── utils/               # MCP utilities
    ├── __init__.py
    ├── validation.py    # Input validation
    └── errors.py        # Error handling
```

**Key Files:**
- `server.py` - Initialize MCP Server with Official MCP SDK
- `tools/*.py` - Individual tool implementations (5 core tools)
- `schemas/tool_schemas.py` - Tool definitions for agent

**Dependencies:**
- Official MCP SDK (`mcp`)
- Phase II persistence (Streamlit storage via `streamlit_app.py`)
- Phase II business logic (validation rules)

---

### 2. Agent (`agent/`)

**Responsibility:** Understand user intent and orchestrate MCP tool calls.

```
agent/
├── __init__.py          # Package initialization
├── agent.py             # OpenAI Agent initialization
├── config/              # Agent configuration
│   ├── __init__.py
│   ├── agent_config.py  # Agent settings and model config
│   └── tool_config.py   # Tool registration for agent
├── prompts/             # System prompts and templates
│   ├── __init__.py
│   ├── system_prompt.py # Main system prompt
│   └── templates.py     # Response templates
└── utils/               # Agent utilities
    ├── __init__.py
    ├── context.py       # Context management
    └── intent.py        # Intent parsing helpers
```

**Key Files:**
- `agent.py` - OpenAI Agent setup with Agents SDK
- `config/agent_config.py` - Model selection, temperature, etc.
- `prompts/system_prompt.py` - Conversational behavior instructions

**Dependencies:**
- OpenAI SDK (`openai`)
- MCP tool schemas
- Environment variables (API keys)

---

### 3. Chat API (`chat_api/`)

**Responsibility:** Orchestrate chat requests between UI, Agent, and MCP Server.

```
chat_api/
├── __init__.py          # Package initialization
├── app.py               # FastAPI app initialization
├── routes/              # API route handlers
│   ├── __init__.py
│   ├── chat.py          # POST /api/chat endpoint
│   └── health.py        # Health check endpoints
├── middleware/          # Request/response middleware
│   ├── __init__.py
│   ├── auth.py          # Authentication middleware
│   └── logging.py       # Request logging
└── schemas/             # Request/response schemas
    ├── __init__.py
    ├── chat_request.py  # Chat request schema
    └── chat_response.py # Chat response schema
```

**Key Files:**
- `app.py` - FastAPI application setup
- `routes/chat.py` - Chat endpoint implementation
- `middleware/auth.py` - JWT authentication from Phase II

**Dependencies:**
- FastAPI (existing Phase II setup)
- OpenAI Agent
- MCP Server
- Phase III persistence

---

### 4. Persistence (`persistence/`)

**Responsibility:** Store and retrieve conversation messages and tool call records.

```
persistence/
├── __init__.py              # Package initialization
├── database.py              # Database connection (Streamlit storage)
├── models/                  # Data models
│   ├── __init__.py
│   ├── conversation.py      # Message model
│   └── tool_call.py         # Tool call record model
└── repositories/            # Data access layer
    ├── __init__.py
    ├── conversation_repo.py # Message CRUD operations
    └── tool_call_repo.py    # Tool call CRUD operations
```

**Key Files:**
- `database.py` - Extend Streamlit storage for conversations
- `models/conversation.py` - Message schema
- `repositories/conversation_repo.py` - Message storage/retrieval

**Dependencies:**
- Streamlit storage (Phase II `todo.db`)
- SQLite3 (Python built-in)

---

### 5. Tests (`tests/`)

**Responsibility:** Comprehensive testing for Phase III components.

```
tests/
├── __init__.py          # Package initialization
├── unit/                # Unit tests
│   ├── __init__.py
│   ├── test_mcp_tools.py        # MCP tool unit tests
│   ├── test_agent.py            # Agent unit tests
│   ├── test_persistence.py      # Persistence unit tests
│   └── test_chat_api.py         # Chat API unit tests
├── integration/         # Integration tests
│   ├── __init__.py
│   ├── test_end_to_end.py       # Full stack tests
│   ├── test_agent_mcp.py        # Agent + MCP integration
│   └── test_chat_flow.py        # Chat flow tests
└── fixtures/            # Test fixtures and mocks
    ├── __init__.py
    ├── mock_agent.py            # Mock agent responses
    ├── mock_mcp.py              # Mock MCP tool responses
    └── test_data.py             # Test conversation data
```

**Key Files:**
- `unit/test_mcp_tools.py` - Test each MCP tool independently
- `integration/test_end_to_end.py` - Test complete user flow
- `fixtures/` - Reusable test data and mocks

---

## Frontend Structure (Chat UI)

Located in: `E:\heckathon-2\frontend\src`

```
frontend/src/
├── app/
│   └── chat/            # Chat page route
│       └── page.tsx     # Chat interface page
├── components/
│   └── chat/            # Chat UI components
│       ├── ChatInterface.tsx     # Main chat component
│       ├── MessageList.tsx       # Message display
│       ├── MessageInput.tsx      # User input
│       └── MessageBubble.tsx     # Individual message
├── contexts/
│   └── chat/            # Chat state management
│       └── ChatContext.tsx       # Chat context provider
├── hooks/
│   └── chat/            # Chat custom hooks
│       ├── useChat.ts            # Chat API integration
│       └── useChatHistory.ts     # History management
├── types/
│   └── chat/            # TypeScript types
│       └── chat.ts               # Chat message types
└── lib/
    └── chat/            # Chat utilities
        └── api.ts                # Chat API client
```

**Key Files:**
- `app/chat/page.tsx` - Chat page (OpenAI ChatKit integration)
- `components/chat/ChatInterface.tsx` - Main chat UI
- `hooks/chat/useChat.ts` - Chat API hook

---

## Separation from Phase II

### Phase II Components (Preserved, Not Modified)

```
E:\heckathon-2\
├── streamlit_app.py     # Phase II Streamlit UI (preserved)
├── todo.db              # Phase II Streamlit storage (extended)
├── backend/             # Phase II FastAPI backend (preserved)
│   └── app/             # Phase II models, routes, services
├── frontend/            # Phase II Next.js frontend (preserved)
│   └── src/app/         # Phase II pages (login, dashboard)
└── phase_i/             # Phase I code (preserved)
```

### Phase III Components (New, Isolated)

```
E:\heckathon-2\
├── phase_iii/           # ALL Phase III code here
│   ├── mcp_server/
│   ├── agent/
│   ├── chat_api/
│   └── persistence/
└── frontend/src/
    ├── app/chat/        # New chat page
    └── components/chat/ # New chat components
```

### Integration Points

**Phase III accesses Phase II via:**
1. **Storage:** Phase III persistence extends `todo.db` (adds tables)
2. **Authentication:** Phase III reuses Phase II JWT authentication
3. **Business Logic:** MCP Server calls Phase II todo operations

**Phase II remains functional:**
- Streamlit UI still works independently
- FastAPI backend still serves REST endpoints
- Frontend dashboard still accessible

---

## Import Path Configuration

### Python Imports (Backend)

**Phase III imports:**
```python
# Within phase_iii package
from phase_iii.mcp_server import tools
from phase_iii.agent import agent
from phase_iii.persistence import repositories

# Absolute imports from project root
from phase_iii.mcp_server.tools.create_todo import CreateTodoTool
from phase_iii.agent.agent import TodoAgent
from phase_iii.persistence.repositories.conversation_repo import ConversationRepository
```

**Phase II imports (from Phase III):**
```python
# Import Phase II storage functions
from streamlit_app import create_todo, get_user_todos, update_todo, delete_todo

# Import Phase II backend models (if needed)
import sys
sys.path.insert(0, './backend')
from app.models.user import User
from app.models.task import Task
```

### TypeScript Imports (Frontend)

**Phase III chat imports:**
```typescript
// Chat components
import { ChatInterface } from '@/components/chat/ChatInterface'
import { useChat } from '@/hooks/chat/useChat'
import { ChatMessage } from '@/types/chat/chat'

// Chat API
import { sendChatMessage } from '@/lib/chat/api'
```

**Phase II imports (preserved):**
```typescript
// Existing components
import { Navbar } from '@/components/Navbar'
import { useAuth } from '@/contexts/AuthContext'
import { Task } from '@/types/api'
```

---

## Development Workflow

### Running Phase III Components

**1. MCP Server:**
```bash
cd E:\heckathon-2
python -m phase_iii.mcp_server.server
```

**2. Chat API (FastAPI):**
```bash
cd E:\heckathon-2
python -m phase_iii.chat_api.app
# Or: uvicorn phase_iii.chat_api.app:app --reload
```

**3. Frontend (with Chat UI):**
```bash
cd E:\heckathon-2\frontend
npm run dev
```

**4. Phase II (Still Works):**
```bash
# Streamlit UI
streamlit run streamlit_app.py

# Phase II Backend
cd backend && uvicorn app.main:app --reload
```

### Testing Phase III

```bash
# Unit tests
pytest phase_iii/tests/unit/

# Integration tests
pytest phase_iii/tests/integration/

# All Phase III tests
pytest phase_iii/tests/

# With coverage
pytest phase_iii/tests/ --cov=phase_iii --cov-report=html
```

---

## Environment Variables

Phase III uses `.env` in project root:

```bash
# OpenAI Agent
OPENAI_API_KEY=your-key

# MCP Server
MCP_SERVER_PORT=5000

# Chat API
CHAT_ENDPOINT_PATH=/api/chat

# Database (Phase II extended)
DATABASE_PATH=todo.db
```

---

## Next Steps

### Immediate Tasks (Phase 1)

1. **Task 1.1-1.6:** Implement persistence layer extensions
   - Conversation message storage
   - Tool call record storage

### Following Tasks (Phase 2)

2. **Task 2.1-2.8:** Implement MCP Server
   - Initialize with Official MCP SDK
   - Implement 5 core tools

3. **Task 3.1-3.10:** Configure OpenAI Agent
   - Initialize with OpenAI SDK
   - Configure tool calling

4. **Task 4.1-4.7:** Implement Chat API endpoints
   - FastAPI chat endpoint
   - Agent invocation

5. **Task 5.1-5.7:** Implement Chat UI
   - OpenAI ChatKit integration
   - Message display and input

---

## Architecture Compliance

This structure adheres to **PHASE_III_CONSTITUTION.md**:

- ✅ **Stateless Architecture:** No runtime state in components
- ✅ **Tool-Based Data Access:** Agent only uses MCP tools
- ✅ **Separation of Concerns:** Clear layer boundaries
- ✅ **Phase II Integration:** Extends without breaking
- ✅ **Spec-Driven Development:** Matches PHASE_III_PLAN.md

---

**Phase III Project Structure - Ready for Implementation**
