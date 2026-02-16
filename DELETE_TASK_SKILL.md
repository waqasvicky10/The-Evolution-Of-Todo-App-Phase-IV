# DeleteTask Skill - Documentation

## Overview

The **DeleteTask Skill** enables the chatbot to delete tasks based on user requests, supporting both specific IDs and name-based identification.

- **Input**: "remove task 3" or "Delete the meeting task"
- **Extraction**:
  - `task_id`: 3 (if provided)
  - `search_term`: "meeting" (if no ID is found)
- **Action**: Call MCP tool `delete_task(user_id, task_id)`
- **Confirmation**: "Task deleted permanently."

## Usage

### In Conversational Context

When a user says:
> "Remove the shopping list task"

The chatbot will:
1. Parse the intent and extract `search_term`: "shopping list".
2. Match the name to an ID (using `list_tasks`).
3. Call the `delete_task` tool.
4. Respond with:
   > "Task deleted permanently."

## Technical Implementation

### 1. Name & ID Parser

Location: [`backend/app/core/task_parser.py`](file:///f:/heckathon-3/backend/app/core/task_parser.py)

- `extract_task_id(text)`: Finds numeric IDs.
- `extract_search_term(text)`: Strips removal prefixes (delete, remove, cancel) and suffixes (task, todo) to find the core task name.

### 2. MCP Tool: `remove_task`

Location: [`phase_iii/mcp_server/tools/todo_tools.py`](file:///f:/heckathon-3/phase_iii/mcp_server/tools/todo_tools.py)

- **Actual Tool**: `delete_todo_tool` (aliased to `remove_task_tool`)
- **Arguments**:
  - `user_id` (int): Required
  - `todo_id` (int): Required
- **Behavior**: Deletes the specified task from the database permanently.

### 3. Chat Integration

Location: [`backend/app/api/routes/chat.py`](file:///f:/heckathon-3/backend/app/api/routes/chat.py)

The `execute_tool_calls_async` function handles both `remove_task` and `delete_todo` to return the unified confirmation message: "Task deleted permanently.".

## Testing

Run the test suite:

```bash
cd f:\heckathon-3\backend
python test_delete_task_skill.py
```

**Test Coverage:**
- ✅ Identification of IDs vs Names
- ✅ Parsing of various deletion prefixes (remove my, delete the, etc.)
- ✅ MCP tool alias availability
- ✅ Specific confirmation message pattern
