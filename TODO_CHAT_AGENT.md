# TodoChatAgent - Main Chatbot Agent

## Role
The **TodoChatAgent** is the central orchestrator for the Todo App's conversational interface. It manages all user interactions, identifies intents, and executes appropriate skills through MCP tools.

## Key Features

### 1. Mandatory Initial Authentication
The agent is strictly instructed to call `get_user_context(user_id)` as its very first action for every message. This ensures it always has access to the user's latest metadata (email, name) for personalized greetings and context.

### 2. Full Skill Integration
The agent orchestrates the following skills:
- **AddTask**: Create new tasks using natural language.
- **ListTasks**: View current tasks with status filtering.
- **CompleteTask**: Mark tasks as done.
- **DeleteTask**: Permanently remove tasks with mandatory confirmation prompts.
- **UpdateTask**: Rename or modify existing task descriptions.
- **SearchTasks**: Advanced filtering by priority, category, and keywords.

### 3. Native Urdu Support
The agent detects Urdu input and responds fluently in Urdu, maintaining all tool-calling capabilities and confirmation patterns.

### 4. Professional Confirmation Patterns
All destructive or state-changing actions are confirmed with specific, user-friendly messages:
- `"Task deleted permanently."`
- `"Task added successfully."`
- `"Task updated successfully."`

## Technical Architecture

- **Provider**: `OpenAIProvider` (using GPT-4o-mini) with a specialized system prompt.
- **System Prompt**: Located in [`backend/app/core/agent_prompts.py`](file:///f:/heckathon-3/backend/app/core/agent_prompts.py).
- **Tool Registry**: MCP Server ([`server.py`](file:///f:/heckathon-3/phase_iii/mcp_server/server.py)) provides the bridge to backend services.
- **Summarization**: [`agent.py`](file:///f:/heckathon-3/phase_iii/agent/agent.py) handles the transformation of structured tool results into natural language.

## Verification

Tests in [`test_todo_chat_agent.py`](file:///f:/heckathon-3/backend/test_todo_chat_agent.py) verify:
- ✅ System prompt injection.
- ✅ Tool call extraction for authentication.
- ✅ Urdu message pass-through.
- ✅ Correct summarization of tool results.
