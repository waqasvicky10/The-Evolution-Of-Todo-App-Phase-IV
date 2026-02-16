# ListTasks Skill - Documentation

## Overview

The **ListTasks Skill** enables the chatbot to return a beautifully formatted list of tasks based on user filters (all, pending, or completed).

- **Input**: "Show my pending tasks"
- **Extraction**: status: "pending"
- **Action**: Call MCP tool `list_tasks(user_id, status="pending")`
- **Output**: A formatted list with IDs and emojis (⏳ for pending, ✅ for completed).

## Usage

### In Conversational Context

When a user says:
> "What are my completed tasks?"

The chatbot will:
1. Parse the intent and extract `status`: "completed".
2. Call the `list_tasks` tool.
3. Respond with:
   > "Here are your completed tasks:
   > ✅ **ID: 101** - buy milk
   > ✅ **ID: 105** - call mom"

## Technical Implementation

### 1. Status Parser

Location: [`backend/app/core/task_parser.py`](file:///f:/heckathon-3/backend/app/core/task_parser.py)

The `parse_list_status(text)` function identifies "pending", "completed", or "all" based on keyword matching in the user input.

### 2. MCP Tool: `list_tasks`

Location: [`phase_iii/mcp_server/tools/todo_tools.py`](file:///f:/heckathon-3/phase_iii/mcp_server/tools/todo_tools.py)

- **Actual Tool**: `list_todos_tool` (aliased to `list_tasks_tool`)
- **Arguments**:
  - `user_id` (int): Required
  - `status` (str): Optional ("all", "pending", "completed")
- **Behavior**: Maps the status string to the internal boolean `completed` filter.

### 3. Chat Integration & Formatting

Location: [`backend/app/api/routes/chat.py`](file:///f:/heckathon-3/backend/app/api/routes/chat.py)

The `execute_tool_calls_async` function handles the `list_tasks` call and generates a Markdown-formatted message with:
- Bold IDs: `**ID: X**`
- Status Emojis: ⏳/✅

## Testing

Run the test suite:

```bash
cd f:\heckathon-3\backend
python test_list_tasks_skill.py
```

**Test Coverage:**
- ✅ Status extraction logic (pending vs completed false positives fixed)
- ✅ MCP tool alias verification
- ✅ Beautiful Markdown list formatting
