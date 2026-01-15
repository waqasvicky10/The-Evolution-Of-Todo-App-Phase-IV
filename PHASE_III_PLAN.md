# PHASE III PLAN
## The Evolution of Todo App - AI-Powered Todo Chatbot

### Document Purpose
This plan defines HOW the Phase III AI-Powered Todo Chatbot will be built. It describes the system architecture, component responsibilities, data flows, and design strategies without specifying implementation details, code, or APIs. All design decisions align with PHASE_III_CONSTITUTION.md and fulfill PHASE_III_SPECIFICATION.md requirements.

### Governing Documents
- **PHASE_III_CONSTITUTION.md** - Architectural principles and boundaries
- **PHASE_III_SPECIFICATION.md** - Functional requirements (WHAT)

---

## High-Level System Architecture

### Architectural Overview

Phase III extends Phase II with a conversational AI layer while maintaining backward compatibility. The architecture follows a strict layered approach with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    USER (Web Browser)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              PRESENTATION LAYER                              │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         OpenAI ChatKit (Chat UI)                       │  │
│  │  - Message display                                     │  │
│  │  - User input handling                                 │  │
│  │  - Conversation rendering                              │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              API GATEWAY LAYER                               │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │            FastAPI Backend                             │  │
│  │  - Chat endpoint orchestration                         │  │
│  │  - Authentication & session management                 │  │
│  │  - Phase II REST endpoints (existing)                  │  │
│  │  - Request routing                                     │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              AI REASONING LAYER                              │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │      Local Mock Agent                                  │  │
│  │  - Keyword-based intent understanding                  │  │
│  │  - Tool selection logic                                │  │
│  │  - Mock response generation                            │  │
│  │  - Conversation context retrieval                      │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ Tool Calls
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              TOOL EXECUTION LAYER                            │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         MCP Server (Official MCP SDK)                  │  │
│  │  - Todo operation tools                                │  │
│  │  - Tool schema definitions                             │  │
│  │  - Input validation                                    │  │
│  │  - Business logic enforcement                          │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              PERSISTENCE LAYER                               │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │      Streamlit-Based Storage                           │  │
│  │  - Todo data storage                                   │  │
│  │  - Conversation history storage                        │  │
│  │  - Tool call records                                   │  │
│  │  - User data                                           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Architectural Principles Applied

1. **Layered Architecture:** Each layer has distinct responsibilities and communicates only with adjacent layers
2. **Stateless Components:** No runtime state in Agent or MCP Server; all state in persistence layer
3. **Tool-Based Data Access:** Agent never directly accesses storage; only through MCP tools
4. **Separation of Concerns:** Reasoning, execution, and storage are completely decoupled
5. **Backward Compatibility:** Phase II functionality preserved and accessible

---

## Component Responsibilities

### Component 1: Chat UI (OpenAI ChatKit)

#### Primary Responsibility
Provide the user-facing conversational interface for todo management through natural language chat.

#### Key Responsibilities
- **Message Display:**
  - Render conversation history in chronological order
  - Distinguish between user and agent messages visually
  - Display timestamps for messages
  - Support message formatting (lists, emphasis, etc.)

- **User Input Handling:**
  - Capture text input from user
  - Submit messages to FastAPI backend
  - Handle enter/send button interactions
  - Provide input validation (non-empty messages)

- **Conversation Rendering:**
  - Load and display previous conversation history on mount
  - Stream agent responses as they arrive (if supported)
  - Auto-scroll to latest messages
  - Indicate when agent is "thinking" or processing

- **Session Management UI:**
  - Display authenticated user information
  - Provide logout functionality
  - Show connection status

#### What This Component Does NOT Do
- Does NOT implement any AI logic
- Does NOT call MCP tools
- Does NOT access storage directly
- Does NOT perform authentication (delegates to backend)
- Does NOT maintain conversation state beyond what's displayed

#### Data Flow Interface
- **Receives:** Agent response messages from FastAPI
- **Sends:** User input messages to FastAPI
- **Retrieves:** Conversation history from FastAPI on load

### Component 2: FastAPI Chat Endpoint

#### Primary Responsibility
Orchestrate chat interactions between the Chat UI, Local Mock Agent, and persistence layer while enforcing authentication and session management.

#### Key Responsibilities
- **Request Orchestration:**
  - Receive user messages from Chat UI
  - Load relevant conversation history from persistence
  - Construct agent invocation with message and context
  - Invoke Anthropic Agent with user message
  - Receive agent response and tool call records
  - Store new messages and tool calls in persistence
  - Return agent response to Chat UI

- **Authentication & Authorization:**
  - Verify user authentication on every chat request
  - Extract authenticated user identity from session/token
  - Pass user context to Agent and MCP Server
  - Reject unauthenticated requests
  - Enforce user data isolation

- **Session Management:**
  - Maintain user session state (authentication only)
  - Handle session expiration
  - Manage concurrent requests per user

- **Phase II Compatibility:**
  - Keep existing REST endpoints operational
  - Route Phase II requests to existing handlers
  - Share authentication mechanism with Phase II

- **Error Handling:**
  - Catch agent errors and return user-friendly messages
  - Handle tool failures gracefully
  - Log errors for debugging
  - Never expose internal errors to user

#### What This Component Does NOT Do
- Does NOT perform AI reasoning or intent detection
- Does NOT implement todo business logic
- Does NOT directly access storage (except for conversation history retrieval)
- Does NOT maintain conversational state (retrieves from storage)

#### Data Flow Interface
- **Receives:** User messages from Chat UI, agent responses from OpenAI Agent
- **Sends:** Agent invocations with context, responses back to Chat UI
- **Reads:** Conversation history from persistence
- **Writes:** New messages and tool calls to persistence

### Component 3: Anthropic Agent (Claude)

#### Primary Responsibility
Understand user intent from natural language and orchestrate MCP tool calls to fulfill todo management requests.

#### Key Responsibilities
- **Intent Understanding:**
  - Parse natural language user messages
  - Identify underlying intent (create, list, update, complete, delete)
  - Extract parameters from user input (todo titles, IDs, descriptions)
  - Handle various phrasings and synonyms
  - Use conversation context to resolve ambiguities

- **Tool Orchestration:**
  - Select appropriate MCP tool(s) based on intent
  - Prepare tool call parameters from user input
  - Invoke MCP tools through Anthropic tool calling mechanism
  - Chain multiple tool calls if needed (e.g., list then update)
  - Handle tool results and errors

- **Response Generation:**
  - Format tool results into natural language
  - Generate user-friendly confirmations
  - Ask clarifying questions when information is missing
  - Request confirmation for destructive actions (delete)
  - Maintain conversational tone and coherence

- **Context Management:**
  - Receive conversation history from FastAPI
  - Use history to inform current response
  - Resolve references to previous messages ("it", "that task")
  - Maintain conversation flow across multiple turns

#### What This Component Does NOT Do
- Does NOT directly access or manipulate stored data
- Does NOT implement todo CRUD operations
- Does NOT cache todo information
- Does NOT maintain in-memory conversation state
- Does NOT bypass MCP tools

#### Data Flow Interface
- **Receives:** User message + conversation history from FastAPI
- **Sends:** Tool call requests to MCP Server (via Anthropic SDK)
- **Receives:** Tool results from MCP Server
- **Returns:** Natural language response + tool call records to FastAPI

#### Agent Configuration Strategy
- Agent receives tool definitions from MCP Server at initialization
- Agent is instructed to use tools for all data operations
- Agent is configured with prompts emphasizing natural conversation
- Agent is instructed to confirm destructive actions
- Agent has access to user identity context for authorization

### Component 4: MCP Server (Official MCP SDK)

#### Primary Responsibility
Expose todo operations as standardized tools and act as the exclusive gateway to the persistence layer.

#### Key Responsibilities
- **Tool Definition:**
  - Define tool schemas for all todo operations
  - Specify tool names, descriptions, and parameters
  - Version tool definitions for stability
  - Register tools with MCP SDK

- **Tool Execution:**
  - Receive tool calls from Anthropic Agent (via FastAPI)
  - Validate tool parameters
  - Invoke appropriate persistence operations
  - Return structured tool results
  - Handle and return errors

- **Business Logic Enforcement:**
  - Apply Phase II validation rules (from existing business logic)
  - Enforce data integrity constraints
  - Validate user permissions on operations
  - Prevent invalid state transitions

- **Data Gateway:**
  - Translate tool calls into persistence operations
  - Map tool results from persistence data
  - Abstract persistence details from Agent
  - Ensure all data access goes through tools

#### What This Component Does NOT Do
- Does NOT perform AI reasoning or natural language understanding
- Does NOT maintain conversation state
- Does NOT cache todo data (stateless)
- Does NOT expose direct database access
- Does NOT implement chat or UI logic

#### Data Flow Interface
- **Receives:** Tool call requests from Agent (via FastAPI)
- **Sends:** Persistence operations to Streamlit storage
- **Receives:** Data from persistence layer
- **Returns:** Structured tool results to Agent

#### Tool Design Strategy
Tools are designed to mirror the five core conversational capabilities:
1. Create todo tool
2. List todos tool
3. Update todo tool
4. Complete todo tool
5. Delete todo tool

Each tool accepts user context for authorization and returns structured results.

### Component 5: Persistence Layer (Streamlit-Based Storage)

#### Primary Responsibility
Provide durable storage for todos, conversation history, and tool call records using Streamlit's storage mechanisms.

#### Key Responsibilities
- **Todo Storage:**
  - Store todo items with all attributes (title, description, status, timestamps, user ID)
  - Support CRUD operations via MCP Server
  - Maintain data integrity
  - Enforce user data isolation
  - Preserve Phase II data schema

- **Conversation History Storage:**
  - Store all user and agent messages
  - Include timestamps and message IDs
  - Link messages to user accounts
  - Support chronological retrieval
  - Enable efficient querying for recent history

- **Tool Call Records Storage:**
  - Store tool invocation records
  - Link tool calls to conversation messages
  - Record tool parameters and results
  - Support audit and debugging queries

- **Data Retrieval:**
  - Provide query interfaces for MCP Server
  - Support filtering by user, date, status
  - Return data in expected formats
  - Handle concurrent access

#### What This Component Does NOT Do
- Does NOT implement business logic
- Does NOT perform authentication or authorization (trusts MCP Server)
- Does NOT communicate with Agent directly
- Does NOT format data for UI presentation

#### Data Flow Interface
- **Receives:** CRUD operations from MCP Server
- **Returns:** Data results to MCP Server
- **Accessed By:** Only MCP Server (exclusive gateway)

#### Storage Strategy
- Leverage Streamlit's session state and file-based persistence
- Use same storage approach as Phase II for todos
- Extend storage schema to include conversation messages and tool calls
- Maintain atomic write operations for data integrity
- Support concurrent read access

---

## Request/Response Flow

### End-to-End Flow: User Sends Chat Message

This section describes the complete journey of a user message through the system, from input to response.

#### Flow Diagram

```
User Types Message
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Chat UI Captures Input                              │
│  - User types: "Add a task to buy groceries"                │
│  - Chat UI sends HTTP POST to FastAPI chat endpoint         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: FastAPI Authenticates and Prepares Context          │
│  - Verify user authentication (session/token)               │
│  - Extract user_id from auth context                        │
│  - Query persistence for recent conversation history        │
│  - Construct agent request with:                            │
│    * Current message                                         │
│    * Conversation history (last N messages)                 │
│    * User context                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Agent Receives Message and Context                  │
│  - Agent analyzes: "Add a task to buy groceries"            │
│  - Intent detected: CREATE_TODO                             │
│  - Parameters extracted: title="Buy groceries"              │
│  - Agent decides to call create_todo tool                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Agent Invokes MCP Tool                              │
│  - Tool call: create_todo(title="Buy groceries", user_id)   │
│  - Anthropic SDK sends tool call to FastAPI             │
│  - FastAPI routes tool call to MCP Server                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: MCP Server Executes Tool                            │
│  - Validate parameters                                       │
│  - Verify user_id authorization                             │
│  - Apply business logic (Phase II validation)               │
│  - Call persistence layer to create todo                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 6: Persistence Layer Stores Data                       │
│  - Generate unique todo ID                                   │
│  - Create todo record with:                                  │
│    * id, title, description, status=pending                 │
│    * created_at, updated_at timestamps                      │
│    * user_id for isolation                                   │
│  - Write to Streamlit storage                               │
│  - Return created todo object                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 7: MCP Server Returns Tool Result                      │
│  - Format tool result:                                       │
│    {                                                         │
│      "success": true,                                        │
│      "todo": {                                               │
│        "id": "123",                                          │
│        "title": "Buy groceries",                            │
│        "status": "pending",                                  │
│        "created_at": "2026-01-06T10:30:00Z"                 │
│      }                                                       │
│    }                                                         │
│  - Return to Agent via FastAPI                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 8: Agent Generates Natural Language Response           │
│  - Agent receives tool result                                │
│  - Agent generates response:                                 │
│    "I've added 'Buy groceries' to your todo list.           │
│     The task is now pending."                               │
│  - Agent returns response to FastAPI                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 9: FastAPI Persists Conversation                       │
│  - Store user message in persistence:                        │
│    * role=user, content="Add task to buy groceries"         │
│    * timestamp, user_id                                      │
│  - Store agent response in persistence:                      │
│    * role=assistant, content="I've added..."                │
│    * timestamp, user_id                                      │
│  - Store tool call record:                                   │
│    * tool_name=create_todo                                   │
│    * parameters, result, timestamp                          │
│    * linked to agent message                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 10: FastAPI Returns Response to Chat UI                │
│  - Send agent response to Chat UI                           │
│  - Chat UI renders agent message                            │
│  - User sees: "I've added 'Buy groceries' to your todo..."  │
└─────────────────────────────────────────────────────────────┘
```

#### Flow Characteristics

**Synchronous vs Asynchronous:**
- User request is synchronous (waits for response)
- Internal tool calls may be asynchronous depending on Agents SDK
- Conversation persistence happens before response is returned

**Error Handling at Each Step:**
- Chat UI: Handle network errors, show retry option
- FastAPI: Catch auth failures, agent errors, persistence errors
- Agent: Handle tool failures, ask clarifying questions
- MCP Server: Validate inputs, return structured errors
- Persistence: Handle write failures, return error codes

**State Management:**
- No state held in memory between requests
- Each request retrieves conversation context from persistence
- Tool calls are independent and stateless
- User authentication is the only session state maintained

### Multi-Turn Conversation Flow

When a conversation requires multiple turns (e.g., clarification, confirmation), the flow repeats:

1. User sends initial message (ambiguous or incomplete)
2. Agent responds with clarifying question (no tool call yet)
3. Conversation stored (user message + agent question)
4. User responds with clarification
5. Agent now has sufficient information
6. Agent invokes tool
7. Agent responds with confirmation
8. Conversation stored (all messages)

The conversation history grows with each turn, providing context for subsequent requests.

---

## MCP Design

### MCP Tool Architecture

The MCP Server exposes five core tools corresponding to the conversational capabilities defined in the specification.

### Tool 1: Create Todo Tool

#### Tool Purpose
Create a new todo item for the authenticated user.

#### Tool Schema Elements
- **Tool Name:** create_todo
- **Description:** Creates a new todo item with the provided details
- **Parameters:**
  - title (required, string): The title/description of the todo
  - description (optional, string): Additional details about the todo
  - due_date (optional, string/date): When the todo is due
  - user_id (required, string): Authenticated user identifier (provided by system)

#### Tool Execution Flow
1. Receive tool call with parameters
2. Validate required parameters (title, user_id)
3. Apply business logic validation (title length, format, etc.)
4. Construct todo object with defaults (status=pending, timestamps)
5. Call persistence layer to store todo
6. Return structured result with created todo details

#### Tool Result Format
- Success: Return todo object with ID, title, status, timestamps
- Failure: Return error with code and user-friendly message

### Tool 2: List Todos Tool

#### Tool Purpose
Retrieve all todos for the authenticated user, optionally filtered.

#### Tool Schema Elements
- **Tool Name:** list_todos
- **Description:** Retrieves the user's todo list with optional filtering
- **Parameters:**
  - user_id (required, string): Authenticated user identifier
  - status (optional, enum): Filter by status (pending, completed, all)
  - due_date_filter (optional, string): Filter by due date (today, this_week, overdue, etc.)
  - limit (optional, integer): Maximum number of todos to return
  - offset (optional, integer): Pagination offset

#### Tool Execution Flow
1. Receive tool call with parameters
2. Validate user_id
3. Construct query with filters
4. Call persistence layer to retrieve todos
5. Apply any additional filtering or sorting
6. Return structured result with todo list

#### Tool Result Format
- Success: Return array of todo objects with count
- Failure: Return error with code and message

### Tool 3: Update Todo Tool

#### Tool Purpose
Update an existing todo item's attributes.

#### Tool Schema Elements
- **Tool Name:** update_todo
- **Description:** Updates an existing todo with new information
- **Parameters:**
  - todo_id (required, string): Unique identifier of the todo to update
  - user_id (required, string): Authenticated user identifier
  - title (optional, string): New title
  - description (optional, string): New description
  - due_date (optional, string/date): New due date
  - status (optional, enum): New status (pending, completed)

#### Tool Execution Flow
1. Receive tool call with parameters
2. Validate todo_id and user_id
3. Verify todo belongs to user (authorization)
4. Validate new values
5. Apply business logic (status transitions, etc.)
6. Call persistence layer to update todo
7. Return structured result with updated todo

#### Tool Result Format
- Success: Return updated todo object
- Failure: Return error (not found, unauthorized, validation failed)

### Tool 4: Complete Todo Tool

#### Tool Purpose
Mark a todo item as completed (specialized update operation).

#### Tool Schema Elements
- **Tool Name:** complete_todo
- **Description:** Marks a todo item as completed
- **Parameters:**
  - todo_id (required, string): Unique identifier of the todo
  - user_id (required, string): Authenticated user identifier

#### Tool Execution Flow
1. Receive tool call with parameters
2. Validate todo_id and user_id
3. Verify todo belongs to user
4. Update status to completed
5. Update updated_at timestamp
6. Call persistence layer to save
7. Return structured result

#### Tool Result Format
- Success: Return updated todo with status=completed
- Failure: Return error (not found, unauthorized, already completed)

### Tool 5: Delete Todo Tool

#### Tool Purpose
Permanently delete a todo item.

#### Tool Schema Elements
- **Tool Name:** delete_todo
- **Description:** Permanently deletes a todo item (cannot be undone)
- **Parameters:**
  - todo_id (required, string): Unique identifier of the todo
  - user_id (required, string): Authenticated user identifier
  - confirmed (optional, boolean): Confirmation flag (agent sets after user confirms)

#### Tool Execution Flow
1. Receive tool call with parameters
2. Validate todo_id and user_id
3. Verify todo belongs to user
4. Check confirmation flag (agent responsibility to set)
5. Call persistence layer to delete
6. Return structured result

#### Tool Result Format
- Success: Return confirmation message with deleted todo ID
- Failure: Return error (not found, unauthorized, not confirmed)

### MCP-Persistence Interaction Strategy

#### How MCP Calls Persistence
- MCP Server imports persistence layer modules
- MCP tool functions call persistence CRUD functions
- Persistence functions are synchronous or async (depending on storage mechanism)
- MCP receives data objects from persistence
- MCP transforms persistence objects into tool result format

#### Data Mapping
- Tool parameters → Persistence function arguments
- Persistence objects → Tool result objects
- Errors from persistence → Tool error responses

#### Business Logic Location
- Validation logic resides in MCP Server (reuse Phase II logic)
- Persistence layer only enforces data integrity (schema, constraints)
- No business logic duplication

---

## Stateless Design Strategy

### Principle: No Runtime State

The system is designed so that no component maintains conversational or operational state in memory beyond a single request-response cycle.

### What is Persisted (Stored in Persistence Layer)

#### 1. Todo Data
- All todo items with full attributes
- User associations
- Timestamps (created, updated)
- Status information

#### 2. Conversation History
- Every user message with timestamp, user_id, content
- Every agent response with timestamp, user_id, content
- Chronological ordering maintained
- Messages linked to user accounts

#### 3. Tool Call Records
- Tool name and invocation timestamp
- Tool parameters (inputs)
- Tool results (outputs)
- Success/failure status
- Linkage to conversation messages

#### 4. User Authentication State
- User sessions (token/cookie-based)
- Authentication credentials (Phase II existing mechanism)
- User profile information

### What is NOT Persisted (Transient)

#### 1. Agent In-Memory State
- No conversation buffers in agent runtime
- No cached intent analysis
- No remembered user preferences in memory
- Agent state resets after each request

#### 2. MCP Server In-Memory State
- No cached todo data
- No session-specific state
- No tool result caches
- Server state resets after each tool call

#### 3. FastAPI Request State
- Request context exists only during request processing
- No conversation state in FastAPI memory
- Authentication session is external (token/cookie)
- No user-specific state in application memory

### How Conversation State is Stored

#### Storage Strategy
1. **Immediate Persistence:** Every message is stored immediately after generation
2. **Atomic Writes:** Each message write is atomic (no partial messages)
3. **Chronological Order:** Messages have timestamps and are retrievable in order
4. **User Isolation:** Messages are scoped to user_id for security

#### Storage Schema Concept
- Conversation messages table/collection with fields:
  - message_id (unique)
  - user_id (foreign key)
  - role (user or assistant)
  - content (text)
  - timestamp (ISO8601)
  - tool_calls (optional array reference)

- Tool calls table/collection with fields:
  - tool_call_id (unique)
  - message_id (foreign key to conversation message)
  - tool_name
  - parameters (JSON/dict)
  - result (JSON/dict)
  - timestamp
  - status (success/failure)

### How Conversation State is Retrieved

#### Retrieval Strategy
1. **On Request:** FastAPI retrieves recent conversation history from persistence when user sends new message
2. **History Window:** System retrieves last N messages (e.g., last 20 messages or last 24 hours)
3. **User-Scoped Query:** Only retrieve messages for authenticated user
4. **Ordered Delivery:** Messages delivered to agent in chronological order

#### Context Injection
- FastAPI constructs agent request payload including:
  - Current user message (new)
  - Historical messages (from persistence)
  - User identity context
- Agent receives full context on every invocation
- Agent uses context to resolve references and maintain conversation flow

### Statelessness Guarantees

#### Reproducibility
- Given same conversation history + same user input → same agent behavior
- Tool calls are deterministic based on input and context
- No hidden state affects decision-making

#### Restartability
- System can restart at any time without losing state
- All state is in persistence, not in memory
- Conversations resume exactly where they left off

#### Scalability
- No per-user memory required in application servers
- Agents can be stateless, horizontally scalable
- MCP Server is stateless, horizontally scalable
- Only persistence layer needs to scale for data volume

---

## Conversation History Handling

### History Storage Design

#### When Messages Are Stored
- User message stored immediately upon receipt by FastAPI (before agent processing)
- Agent response stored immediately after agent returns (before sending to UI)
- Tool call records stored with agent response

#### Storage Location
- Conversation messages stored in persistence layer (same Streamlit storage as todos)
- Tool calls stored in persistence layer, linked to messages

#### Storage Format
- Messages stored as records with structured fields (not raw logs)
- Tool calls stored as structured records with parameters and results
- Timestamps in ISO8601 format for consistency

### History Retrieval Design

#### Retrieval Triggers
- When user sends new message → retrieve recent history for agent context
- When user opens chat UI → retrieve history for display
- When user requests history explicitly ("What did I add yesterday?") → agent retrieves via tool or FastAPI query

#### Retrieval Scope
- Retrieve last N messages (configurable, e.g., 50 messages)
- OR retrieve messages from last M hours (configurable, e.g., 24 hours)
- Always user-scoped (only authenticated user's messages)

#### Retrieval Performance
- Index conversation messages by user_id and timestamp
- Queries optimized for recent message retrieval
- Pagination support for long histories

### History Context Window Strategy

#### Why Limit Context?
- Agent models have token limits
- Recent context is more relevant than old context
- Performance and cost optimization

#### Context Window Size
- Default: Last 20-50 messages (sufficient for most conversations)
- Configurable based on model context limits
- System includes current message + history within window

#### Handling Long Conversations
- If conversation exceeds context window, older messages are not included
- Agent operates on recent history only
- Full history still accessible for display in UI
- Agent may request specific older information via summarization tool (optional future enhancement)

### Cross-Session History Continuity

#### How Cross-Session Works
1. User completes session and closes chat
2. All messages already persisted
3. User opens chat in new session (same day or later)
4. FastAPI loads conversation history from persistence
5. Chat UI displays full history
6. When user sends new message, agent receives recent history as context
7. Agent can reference previous session naturally

#### Session Boundary Handling
- No explicit "session start" or "session end" markers
- Conversation is continuous across sessions
- Time gaps between messages are preserved in timestamps
- Agent can recognize time gaps and adjust responses accordingly

---

## Error Handling Strategy

### Error Categories

Phase III error handling addresses three primary error categories:

1. **Tool Failures:** MCP tool calls fail or return errors
2. **Invalid Intent:** Agent cannot understand user input or map to tools
3. **Authentication Issues:** User authorization fails or session expires

### Error Category 1: Tool Failures

#### Sources of Tool Failures
- Persistence layer unavailable or returns error
- Data validation fails in MCP Server
- Business logic constraints violated
- Network or system errors during tool execution

#### Detection
- MCP tool returns error result instead of success
- Agent receives error from tool call
- FastAPI catches exceptions from MCP or persistence

#### Handling Strategy

**At MCP Server Level:**
- Catch persistence errors
- Validate inputs and return validation errors
- Return structured error responses (error_code, error_message)
- Log errors for debugging

**At Agent Level:**
- Receive error result from tool
- Interpret error code/message
- Generate user-friendly explanation (no technical jargon)
- Suggest corrective action if possible

**Example Flow:**
```
User: "Delete the grocery task"
Agent: [calls delete_todo tool]
MCP Server: [todo not found in persistence]
MCP Server: [returns error: "not_found"]
Agent: [receives error]
Agent: "I couldn't find a task matching 'grocery task'. Would you like to see your current tasks?"
```

**At FastAPI Level:**
- Catch unhandled exceptions from agent or MCP
- Return generic error message to UI
- Log full error details for investigation
- Never expose internal error details to user

### Error Category 2: Invalid Intent

#### Sources of Invalid Intent
- User input is nonsensical or off-topic
- User requests functionality not supported (e.g., "send email")
- User input is ambiguous and agent cannot resolve
- User references non-existent todos or data

#### Detection
- Agent cannot map user input to any tool
- Agent attempts tool call but user provides insufficient information
- Agent recognizes request is out of scope

#### Handling Strategy

**At Agent Level:**
- Recognize when no tool matches user intent
- Generate clarifying question or helpful response
- Explain capabilities if user seems confused
- Politely decline if request is out of scope

**Example Flows:**
```
User: "qwerty asdf"
Agent: "I'm not sure I understood that. I can help you add, view, update, complete, or delete todos. What would you like to do?"
```

```
User: "Send email to my team"
Agent: "I can't send emails, but I can help you manage your todo list. Would you like to add a reminder to email your team?"
```

```
User: "Update the task"
Agent: "I found 5 tasks. Which one would you like to update?"
```

**At FastAPI Level:**
- No special handling needed (agent handles gracefully)
- Log conversation for quality monitoring

### Error Category 3: Authentication Issues

#### Sources of Authentication Issues
- User not logged in (session expired or never authenticated)
- User attempts to access another user's data
- Authentication token invalid or tampered

#### Detection
- FastAPI authentication middleware rejects request
- MCP Server verifies user_id authorization and detects mismatch
- Session validation fails

#### Handling Strategy

**At FastAPI Level (Primary):**
- Authentication middleware checks every chat request
- Reject unauthenticated requests with 401 Unauthorized
- Redirect to login page or return auth error to UI
- Never allow chat access without valid authentication

**At MCP Level (Secondary):**
- Verify user_id matches todo ownership
- Reject tool calls attempting cross-user access
- Return authorization error to agent
- Log security-relevant events

**At Chat UI Level:**
- Detect authentication errors from FastAPI
- Redirect user to login page
- Display session expiration message
- Clear any cached UI state

**Example Flow:**
```
User: [session expired] "Show my tasks"
FastAPI: [auth check fails]
FastAPI: [returns 401 Unauthorized]
Chat UI: [receives 401]
Chat UI: "Your session has expired. Please log in again."
Chat UI: [redirects to login]
```

### Error Logging and Monitoring

#### What to Log
- All tool failures with error codes and messages
- All authentication failures
- Agent errors or unexpected responses
- Persistence layer errors
- Request/response payloads for failed requests (sanitized)

#### Where to Log
- FastAPI application logs (request/response level)
- MCP Server logs (tool execution level)
- Persistence layer logs (data operation level)
- Agent framework logs (if supported)

#### Log Retention
- Logs retained for debugging and audit
- No sensitive user data in logs (sanitize)
- Errors linked to request IDs for tracing

---

## Security Considerations

### Authentication Context Propagation

#### Authentication at Entry Point
- User authenticates with FastAPI (Phase II existing mechanism)
- FastAPI verifies credentials and establishes session
- Session token/cookie issued to user
- All subsequent requests include session token

#### Propagating User Identity

**From Chat UI to FastAPI:**
- Chat UI includes session token in request headers (cookie or Authorization header)
- FastAPI validates token on every request
- FastAPI extracts user_id from validated token

**From FastAPI to Agent:**
- FastAPI includes user_id in agent invocation context
- Agent receives user_id but does not use it directly for data access
- Agent includes user_id in tool call parameters

**From Agent to MCP Server:**
- Tool calls include user_id as parameter
- MCP Server receives user_id and uses it for authorization
- MCP Server passes user_id to persistence layer

**From MCP Server to Persistence:**
- Persistence queries filtered by user_id
- All CRUD operations scoped to user_id
- No cross-user data retrieval possible

#### Security Guarantees
- User identity verified once at entry (FastAPI)
- User identity propagated through all layers
- Each layer trusts previous layer's authentication
- MCP Server enforces authorization (data ownership)
- Persistence layer enforces data isolation

### User Data Isolation

#### Isolation Requirements
- Users can only access their own todos
- Users can only see their own conversation history
- Users cannot invoke tools on other users' data
- No cross-user data leakage at any layer

#### Isolation Enforcement

**At FastAPI Level:**
- Session management ensures user_id is correct
- FastAPI retrieves only authenticated user's conversation history
- FastAPI never mixes user contexts

**At Agent Level:**
- Agent receives user_id and includes it in tool calls
- Agent has no access to other users' contexts
- Agent operates in isolated invocation scope

**At MCP Level:**
- MCP Server validates user_id matches todo ownership before operations
- MCP queries always include user_id filter
- MCP rejects unauthorized operations with error

**At Persistence Level:**
- All queries include user_id filter
- Database/storage indexes enforce user_id scoping
- No query can return data without user_id filter

#### Testing Data Isolation
- Integration tests verify cross-user access fails
- Simulate concurrent users with different user_ids
- Verify tool calls reject unauthorized operations
- Verify persistence queries return only user-scoped data

### Secure Tool Execution

#### Input Validation
- MCP Server validates all tool parameters
- Reject malformed, missing, or invalid inputs
- Sanitize inputs to prevent injection attacks
- Validate data types and ranges

#### Authorization Checks
- Verify user_id ownership before every operation
- Reject operations on todos not owned by user
- Return authorization errors, not "not found" (to avoid leaking existence)

#### Output Sanitization
- Tool results do not include sensitive system information
- Error messages are user-friendly, not technical
- No stack traces or internal paths exposed

### Authentication Token Security

#### Token Handling
- Tokens transmitted over HTTPS only
- Tokens stored securely in browser (HttpOnly cookies preferred)
- Tokens have expiration times
- Tokens validated on every request

#### Token Revocation
- Users can log out to invalidate session
- Expired tokens are rejected
- FastAPI maintains session validity

### Rate Limiting and Abuse Prevention

#### Rate Limiting Strategy (Optional, but recommended)
- Limit chat requests per user per minute
- Prevent spam or automated abuse
- Return rate limit errors to UI
- Log excessive request patterns

#### Abuse Detection
- Monitor for unusual tool call patterns
- Detect and block malicious inputs
- Log security events for review

---

## Separation of Concerns Design

### Concern 1: Agent Reasoning (OpenAI Agents SDK)

#### What This Concern Includes
- Understanding user intent from natural language
- Mapping intent to tool calls
- Generating natural language responses
- Maintaining conversational coherence

#### What This Concern Excludes
- Direct data access or storage
- Todo business logic or validation
- Authentication or authorization enforcement
- Persistence operations
- UI rendering or styling

#### Boundaries
- **Input Boundary:** Receives user message + conversation history from FastAPI
- **Output Boundary:** Returns natural language response + tool call records to FastAPI
- **Tool Boundary:** Invokes MCP tools via OpenAI Agents SDK; never bypasses tools

#### Independence
- Agent can be tested with mock MCP tools
- Agent can be replaced with different AI model without affecting MCP or persistence
- Agent does not depend on persistence implementation details

### Concern 2: Tool Execution (MCP SDK)

#### What This Concern Includes
- Defining and exposing todo operation tools
- Validating tool inputs
- Enforcing business logic (Phase II validation rules)
- Executing persistence operations
- Returning structured tool results

#### What This Concern Excludes
- Natural language understanding or generation
- Intent detection or conversational logic
- UI rendering or chat interface
- Authentication (receives user_id, does not authenticate)
- Conversation history management

#### Boundaries
- **Input Boundary:** Receives tool call requests from Agent (via FastAPI)
- **Output Boundary:** Returns structured tool results to Agent
- **Persistence Boundary:** Calls persistence layer for data operations; abstracts storage details

#### Independence
- MCP Server can be tested with mock persistence layer
- MCP tools can be invoked independently of agent
- MCP tool schemas can be versioned and updated without changing agent
- Persistence implementation can change without affecting MCP interface

### Concern 3: Data Persistence (Streamlit Storage)

#### What This Concern Includes
- Storing and retrieving todo data
- Storing and retrieving conversation history
- Storing and retrieving tool call records
- Enforcing data integrity constraints
- Managing database/storage connections

#### What This Concern Excludes
- Business logic or validation (done in MCP layer)
- Authentication or authorization (trusts MCP layer)
- Natural language processing
- Tool orchestration
- User interface logic

#### Boundaries
- **Input Boundary:** Receives CRUD operation calls from MCP Server
- **Output Boundary:** Returns data objects or error codes to MCP Server
- **Access Boundary:** Only accessible via MCP Server (no direct access from Agent or FastAPI)

#### Independence
- Persistence layer can be swapped (e.g., move from Streamlit storage to PostgreSQL) without changing MCP interface
- Persistence tested independently with direct CRUD operations
- Schema changes isolated to persistence layer and MCP mapping layer

### Cross-Cutting Concerns

#### Logging
- All layers log relevant events
- Logs are centralized or correlated by request ID
- Each layer logs at its own level of abstraction

#### Error Handling
- Each layer handles its own errors
- Errors propagate up the stack with appropriate abstraction
- User-facing errors are friendly, internal errors are detailed

#### Security
- Authentication happens at API gateway (FastAPI)
- Authorization enforced at MCP layer
- Data isolation enforced at persistence layer

### Benefits of Separation

#### Testability
- Each concern can be unit tested independently
- Integration tests verify boundaries
- Mock implementations enable isolated testing

#### Maintainability
- Changes to one concern do not ripple to others
- Clear responsibility boundaries
- Easy to locate and fix bugs

#### Scalability
- Stateless concerns (Agent, MCP) can scale horizontally
- Persistence layer can scale independently
- No tight coupling between layers

---

## OPTIONAL BONUS FEATURES: Extension Points

This section identifies where optional bonus features may be integrated without violating architectural principles.

### OPTIONAL: Multi-Language Support (Including Urdu)

#### Where This Plugs In
- **Agent Layer:** Agent receives language hint or detects language from user input
- **Response Generation:** Agent generates responses in detected language
- **Tool Calls:** Tool calls remain language-agnostic (structured data)
- **Persistence:** Store language preference per user (optional)

#### Extension Point Design
- Language detection happens in Agent or FastAPI before agent invocation
- Agent prompt includes language context ("Respond in Urdu")
- OpenAI models support multilingual responses natively
- Tool schemas and results remain in English (internal)
- User-facing messages generated in user's language

#### Architectural Compliance
- No changes to MCP tool layer
- No changes to persistence schema (except optional language preference field)
- Stateless: language detected per request or retrieved from user profile
- Tools remain language-agnostic

### OPTIONAL: Voice Input/Output

#### Where This Plugs In
- **Before Chat UI:** Voice input captured and converted to text (speech-to-text)
- **After Agent Response:** Text response converted to voice (text-to-speech)
- **Internally:** All processing uses text (same flow as typed input)

#### Extension Point Design
- Voice capture component in UI (microphone button)
- Speech-to-text service converts audio to text
- Text sent to FastAPI as normal message
- Agent processes text normally
- Agent response converted to speech by text-to-speech service
- Audio played to user

#### Architectural Compliance
- Voice is input/output modality, not separate system
- No changes to Agent, MCP, or persistence layers
- Stateless: each voice input is independent
- Error handling: speech recognition errors treated like unclear text input

### OPTIONAL: Reusable Intelligence via Agent Skills or Subagents

#### Where This Plugs In
- **Agent Layer:** Main agent delegates to specialized subagents for complex tasks
- **Tool Layer:** Subagents may invoke MCP tools (same tools as main agent)
- **FastAPI:** Orchestrates main agent and subagents if needed

#### Extension Point Design
- Main agent recognizes when to delegate (e.g., "Summarize my todos")
- Main agent invokes subagent with specific task
- Subagent processes task using MCP tools
- Subagent returns result to main agent
- Main agent integrates result into response

#### Architectural Compliance
- Subagents MUST use MCP tools for data access (no bypass)
- Subagents are stateless (no persistent memory)
- Subagents tested independently
- Core functionality works without subagents (they are enhancements)

#### Example Subagent: Todo Summarization
- User: "Summarize my todos for this week"
- Main agent: Recognizes summarization task
- Main agent: Invokes summarization subagent
- Subagent: Calls list_todos tool with filter
- Subagent: Analyzes todos and generates summary
- Subagent: Returns summary to main agent
- Main agent: Presents summary to user

---

## Phase II Integration Strategy

### Coexistence Approach

Phase III is additive to Phase II. Both interfaces operate on the same data and coexist peacefully.

### Shared Components

#### Persistence Layer
- Phase II and Phase III use the same Streamlit storage
- Same todo data schema
- Same user authentication storage
- No data duplication

#### Business Logic
- Phase II validation rules reused in Phase III MCP Server
- No logic duplication
- Single source of truth for todo constraints

#### Authentication
- Phase II authentication mechanism extended to Phase III
- Same session management
- Same user accounts

### Independent Components

#### Phase II REST API
- Remains operational and unchanged
- Direct CRUD endpoints for todos
- Used by Phase II UI (if exists)

#### Phase III Chat API
- New endpoint(s) for chat interactions
- Uses OpenAI Agent + MCP architecture
- Independent of Phase II REST logic

### Routing Strategy

FastAPI routes different request types:
- `/api/todos/*` → Phase II REST handlers
- `/api/chat` → Phase III chat handler
- Both share authentication middleware
- Both access same persistence layer

### Data Compatibility

#### Todos Created in Phase II
- Visible and manageable in Phase III chat
- No migration needed
- Same data schema

#### Todos Created in Phase III
- Visible in Phase II REST API responses
- No special handling needed
- Same data schema

### Migration Path

Phase III does not require migration. It is a parallel interface to existing functionality.

---

## Implementation Readiness Checklist

### Before Proceeding to Task Definition, Verify:

- [ ] All components and responsibilities are clearly defined
- [ ] Request/response flows are complete and traceable
- [ ] MCP tool designs align with conversational capabilities
- [ ] Stateless architecture is consistently applied across all components
- [ ] Conversation history storage and retrieval strategy is clear
- [ ] Error handling strategy covers all error categories
- [ ] Security considerations address authentication, authorization, and isolation
- [ ] Separation of concerns is maintained across all layers
- [ ] Optional features are clearly marked and have defined extension points
- [ ] Phase II integration strategy preserves existing functionality
- [ ] All design decisions trace back to Phase III Specification requirements
- [ ] All architectural principles from Phase III Constitution are upheld
- [ ] No implementation details (code, schemas, APIs) are specified
- [ ] Plan is actionable and sufficient for task breakdown

---

## Document Status

**Version:** 1.0
**Status:** ACTIVE
**Created:** 2026-01-06
**Governed By:**
- PHASE_III_CONSTITUTION.md (architectural principles)
- PHASE_III_SPECIFICATION.md (functional requirements)

**Next Document:** PHASE_III_TASKS.md (awaiting creation)

---

## Approval and Sign-Off

This plan defines HOW Phase III will be built architecturally. Detailed implementation (code, schemas, APIs) will be defined in the task breakdown phase.

**Plan Complete. Awaiting approval to proceed to Phase III Task Definition.**

---

**END OF PHASE III PLAN**
