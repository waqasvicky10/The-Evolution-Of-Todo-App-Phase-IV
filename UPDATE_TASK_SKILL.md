# UpdateTask Skill - Documentation

## Overview

The **UpdateTask Skill** allows users to update existing tasks by providing their ID and the new content (title/description) in natural language.

- **Input**: "Change task 2 to Buy milk and eggs"
- **Extraction**:
  - `task_id`: 2
  - `new_content`: "Buy milk and eggs"
- **Action**: Call MCP tool `update_task(user_id, task_id, title, description)`
- **Confirmation**: Shows the updated task details.

## Usage

### In Conversational Context

When a user says:
> "Update item 5: call the doctor"

The chatbot will:
1. Parse the request and extract `task_id` (5) and `new_content` ("call the doctor").
2. Call the `update_task` tool.
3. Respond with:
   > "Task 5 updated successfully: call the doctor"

## Technical Implementation

### 1. Update Parser

Location: [`backend/app/core/task_parser.py`](file:///f:/heckathon-3/backend/app/core/task_parser.py)

The `parse_update_input(text)` function uses flexible regex patterns to extract the ID and everything after separators like "to", "with", or ":".

### 2. MCP Tool: `update_task`

Location: [`phase_iii/mcp_server/tools/todo_tools.py`](file:///f:/heckathon-3/phase_iii/mcp_server/tools/todo_tools.py)

- **Actual Tool**: `update_todo_tool` (aliased to `update_task_tool`)
- **Arguments**:
  - `user_id` (int): Required
  - `todo_id` (int): Required
  - `title` (str): Optional
  - `description` (str): Optional
- **Behavior**: Updates the specified fields for the task in the database.

### 3. Chat Integration

Location: [`backend/app/api/routes/chat.py`](file:///f:/heckathon-3/backend/app/api/routes/chat.py)

The `execute_tool_calls_async` function handles `update_task`, applying the `new_content` as the task description and returning a clear success message.

## Testing

Run the test suite:

```bash
cd f:\heckathon-3\backend
python test_update_task_skill.py
```

**Test Coverage:**
- ✅ ID and content extraction from various formats (to, with, :)
- ✅ Robustness to whitespace
- ✅ MCP tool alias verification
