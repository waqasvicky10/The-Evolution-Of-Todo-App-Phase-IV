# AddTask Skill - Documentation

## Overview

The **AddTask Skill** enables the chatbot to parse natural language requests and create tasks using MCP tools. It implements the following pattern:

- **Input**: "Add a task to buy groceries tomorrow"
- **Extraction**: Title: "buy groceries", Description: "tomorrow"
- **Action**: Call MCP tool `add_task(user_id, title, description)`
- **Confirmation**: "Task added: [Title] (ID: [X])"

## Usage

### In Conversational Context

When a user says:
> "Add a task to call my landlord next Monday"

The chatbot will:
1. Parse the intent and extract:
   - `title`: "call my landlord"
   - `description`: "next Monday"
2. Call the `add_task` tool.
3. Respond with:
   > "Task added: call my landlord (ID: 123)"

## Technical Implementation

### 1. Task Parser

Location: [`backend/app/core/task_parser.py`](file:///f:/heckathon-3/backend/app/core/task_parser.py)

The `parse_task_input(text)` function uses regex to strip common prefixes and extract the title and optional time-based description.

### 2. MCP Tool: `add_task`

Location: [`phase_iii/mcp_server/tools/todo_tools.py`](file:///f:/heckathon-3/phase_iii/mcp_server/tools/todo_tools.py)

- **Actual Tool**: `create_todo_tool` (aliased to `add_task_tool`)
- **Arguments**:
  - `user_id` (int): Required
  - `title` (str): Required
  - `description` (str): Optional
- **Behavior**: Combines `title` and `description` into the database `description` field as `[Title] ([Description])`.

### 3. Chat Integration

Location: [`backend/app/api/routes/chat.py`](file:///f:/heckathon-3/backend/app/api/routes/chat.py)

The `execute_tool_calls_async` function handles the `add_task` tool call and ensures the confirmation message follows the required pattern.

## Testing

Run the test suite:

```bash
cd f:\heckathon-3\backend
python test_add_task_skill.py
```

**Test Coverage:**
- ✅ Extraction of title from natural language
- ✅ Extraction of description (time/context)
- ✅ MCP tool alias verification
- ✅ Confirmation message pattern matching

## FAQ

### Does it support Urdu?
The current implementation of the `AddTask` skill logic is primary focused on English patterns. However, the underlying Phase III agent supports Urdu and can use the tool as well.

### What happens if no description is extracted?
The tool is called with `description=None`, and only the title is stored in the database.
