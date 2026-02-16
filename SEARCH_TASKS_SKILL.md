# SearchTasks Skill - Documentation

## Overview

The **SearchTasks Skill** empowers the chatbot to find and filter tasks based on multiple criteria provided in natural language.

- **Input**: "Show high priority work tasks about meeting"
- **Extraction**:
  - `priority`: "high"
  - `category`: "work"
  - `keyword`: "meeting"
- **Action**: Call MCP tool `search_tasks(user_id, status, priority, category, keyword)`
- **Response**: A beautifully formatted list showing all matching tasks.

## Usage

### In Conversational Context

Users can combine filters:
> "Show my pending shopping tasks"
> "Find high priority urgent items"
> "Display all tasks about project X"

The chatbot will:
1. Parse the request to identify priority levels, categories, and specific keywords.
2. Query the database using dynamic SQL filtering.
3. Present the results with relevant status emojis and priority tags.

## Technical Implementation

### 1. Search Query Parser

Location: [`backend/app/core/task_parser.py`](file:///f:/heckathon-3/backend/app/core/task_parser.py)

- `parse_search_query(text)`: 
  - Detects priority keywords (high, medium, low).
  - Matches against known categories (work, personal, shopping, etc.).
  - Extracts keywords by removing search prefixes and redundant terms.

### 2. MCP Tool: `search_tasks`

Location: [`phase_iii/mcp_server/tools/todo_tools.py`](file:///f:/heckathon-3/phase_iii/mcp_server/tools/todo_tools.py)

- **Actual Tool**: `list_todos_tool` (aliased to `search_tasks_tool` and `list_tasks_tool`)
- **Enhanced Capability**: Now supports `priority`, `category`, and `keyword` arguments.
- **Dynamic SQL**: Builds the `WHERE` clause based on provided filters for efficient retrieval.

### 3. Service & API Layer

- **Service**: `get_user_tasks` in `task_service.py` was updated to support SQLAlchemy-level filtering for priority and category.
- **Chat API**: `chat.py` integrates these filters and adds secondary keyword-based filtering on task descriptions for precision.

## Testing

Run the test suite:

```bash
cd f:\heckathon-3\backend
python test_search_tasks_skill.py
```

**Test Coverage:**
- ✅ Extraction of priority (high/medium/low)
- ✅ Category identification
- ✅ Keyword stripping and isolation
- ✅ MCP tool alias availability
