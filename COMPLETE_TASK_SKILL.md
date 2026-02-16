# CompleteTask Skill - Documentation

## Overview

The **CompleteTask Skill** allows the chatbot to mark specific tasks as completed based on user requests (e.g., "Mark task 5 as done").

- **Input**: "Mark task 5 as done"
- **Extraction**: task_id: 5
- **Action**: Call MCP tool `complete_task(user_id, task_id)`
- **Confirmation**: "Task 5 marked complete ✓"

## Usage

### In Conversational Context

When a user says:
> "I finished task 10"

The chatbot will:
1. Parse the intent and extract `task_id`: 10.
2. Call the `complete_task` tool.
3. Respond with:
   > "Task 10 marked complete ✓"

## Technical Implementation

### 1. ID Parser

Location: [`backend/app/core/task_parser.py`](file:///f:/heckathon-3/backend/app/core/task_parser.py)

The `extract_task_id(text)` function using regex to find numeric IDs associated with keywords like "task", "item", or just standalone numbers.

### 2. MCP Tool: `complete_task`

Location: [`phase_iii/mcp_server/tools/todo_tools.py`](file:///f:/heckathon-3/phase_iii/mcp_server/tools/todo_tools.py)

- **Actual Tool**: `complete_task_tool` (specialized wrapper around `update_todo_tool`)
- **Arguments**:
  - `user_id` (int): Required
  - `todo_id` (int): Required
- **Behavior**: Sets `is_complete=True` for the specified task in the database.

### 3. Chat Integration

Location: [`backend/app/api/routes/chat.py`](file:///f:/heckathon-3/backend/app/api/routes/chat.py)

The `execute_tool_calls_async` function handles the `complete_task` call and returns the specific pattern: "Task [ID] marked complete ✓".

## Testing

Run the test suite:

```bash
cd f:\heckathon-3\backend
python test_complete_task_skill.py
```

**Test Coverage:**
- ✅ Numeric ID extraction from natural language
- ✅ MCP tool registration verification
- ✅ Pattern-matched confirmation message
