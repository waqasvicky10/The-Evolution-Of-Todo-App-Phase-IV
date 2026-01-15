# PHASE III TASKS
## The Evolution of Todo App - AI-Powered Todo Chatbot

### Document Purpose
This document breaks down Phase III implementation into atomic, ordered, testable tasks. Each task is self-contained, clearly defined, and traceable to the Plan and Specification. Tasks are organized by component and dependency order to enable safe, deterministic execution.

### Governing Documents
- **PHASE_III_CONSTITUTION.md** - Architectural principles and boundaries
- **PHASE_III_SPECIFICATION.md** - Functional requirements (WHAT)
- **PHASE_III_PLAN.md** - Architectural design (HOW)

---

## Task Organization Principles

### Task Characteristics
- **Atomic:** Each task has a single, clear responsibility
- **Ordered:** Tasks listed in dependency order (prerequisites first)
- **Testable:** Each task has clear validation criteria
- **Traceable:** Each task references relevant Specification and Plan sections

### Task Execution Rules
- Tasks must be executed in order within each phase
- Tasks within same phase number can be executed in parallel if independent
- No task may be started until prerequisites are complete
- Each task must be validated before proceeding

### Task Status Tracking
- **Not Started:** Task awaiting execution
- **In Progress:** Task currently being implemented
- **Completed:** Task implemented and validated
- **Blocked:** Task cannot proceed (indicate blocker)

---

## PHASE 0: Foundation and Prerequisites

### Task 0.1: Verify Phase II Baseline
**Component:** All
**Prerequisite:** None
**Description:** Verify Phase II todo system is operational and accessible for Phase III extension.

**Acceptance Criteria:**
- [ ] Phase II todo data is accessible via existing storage mechanism
- [ ] Phase II authentication system is functional
- [ ] Phase II user management is operational
- [ ] Streamlit storage is initialized and accessible
- [ ] No Phase II functionality is broken

**References:**
- Plan: Phase II Integration Strategy
- Constitution: Integration with Phase II

**Validation:**
- Run Phase II tests (if exist)
- Manually verify Phase II CRUD operations work
- Confirm storage contains accessible todo data

---

### Task 0.2: Set Up Development Environment
**Component:** All
**Prerequisite:** Task 0.1
**Description:** Install and configure required dependencies for Phase III components.

**Acceptance Criteria:**
- [ ] OpenAI Agents SDK installed
- [ ] Official MCP SDK installed
- [ ] OpenAI ChatKit library installed
- [ ] FastAPI environment updated (if needed)
- [ ] Environment variables configured (API keys, etc.)
- [ ] Development tools installed (linters, formatters)

**References:**
- Plan: High-Level System Architecture
- Constitution: Mandatory Core Stack

**Validation:**
- Import all required libraries successfully
- Verify SDK versions meet requirements
- Confirm environment variables are accessible

---

### Task 0.3: Define Project Structure for Phase III
**Component:** All
**Prerequisite:** Task 0.2
**Description:** Create directory structure and module organization for Phase III components.

**Acceptance Criteria:**
- [ ] Directory structure created for MCP server code
- [ ] Directory structure created for agent configuration
- [ ] Directory structure created for chat UI components
- [ ] Directory structure created for FastAPI chat endpoints
- [ ] Directory structure created for conversation persistence
- [ ] Clear separation maintained from Phase II code
- [ ] Import paths configured correctly

**References:**
- Plan: Component Responsibilities
- Constitution: Separation of Concerns

**Validation:**
- All directories exist and are accessible
- Import paths resolve correctly
- No conflicts with Phase II structure

---

## PHASE 1: Persistence Layer Extensions

### Task 1.1: Design Conversation Message Schema
**Component:** Persistence Layer
**Prerequisite:** Task 0.3
**Description:** Define data schema for storing conversation messages in Streamlit storage.

**Acceptance Criteria:**
- [ ] Message schema includes: id, user_id, role, content, timestamp
- [ ] Schema supports user and assistant roles
- [ ] Timestamp format is ISO8601
- [ ] User_id links to existing user accounts
- [ ] Schema documented in code comments

**References:**
- Specification: Data Requirements - Conversation Messages
- Plan: Persistence Strategy, Stateless Design

**Validation:**
- Schema definition reviewed and approved
- Schema aligns with Streamlit storage capabilities
- All required fields present

---

### Task 1.2: Design Tool Call Record Schema
**Component:** Persistence Layer
**Prerequisite:** Task 1.1
**Description:** Define data schema for storing tool call records in Streamlit storage.

**Acceptance Criteria:**
- [ ] Tool call schema includes: id, message_id, tool_name, parameters, result, timestamp, status
- [ ] Message_id links to conversation messages
- [ ] Parameters and result stored as structured data (JSON/dict)
- [ ] Status field supports success/failure values
- [ ] Schema documented in code comments

**References:**
- Specification: Data Requirements - Tool Call Records
- Plan: Persistence Strategy, Stateless Design

**Validation:**
- Schema definition reviewed and approved
- Schema supports linkage to messages
- Structured data storage verified

---

### Task 1.3: Implement Conversation Message Storage Functions
**Component:** Persistence Layer
**Prerequisite:** Task 1.2
**Description:** Implement functions to create and store conversation messages in Streamlit storage.

**Acceptance Criteria:**
- [ ] Function: store_message(user_id, role, content) → message_id
- [ ] Generates unique message ID
- [ ] Stores message with current timestamp
- [ ] Enforces user_id isolation
- [ ] Returns created message object
- [ ] Atomic write operation
- [ ] Function documented with docstring

**References:**
- Specification: Data Requirements - Conversation Messages
- Plan: Persistence Layer Responsibilities, Stateless Design

**Validation:**
- Unit test: Store message and verify retrieval
- Unit test: Verify unique IDs generated
- Unit test: Verify timestamp accuracy

---

### Task 1.4: Implement Conversation Message Retrieval Functions
**Component:** Persistence Layer
**Prerequisite:** Task 1.3
**Description:** Implement functions to retrieve conversation history from Streamlit storage.

**Acceptance Criteria:**
- [ ] Function: get_recent_messages(user_id, limit=50) → list of messages
- [ ] Retrieves messages in chronological order
- [ ] Filters by user_id (data isolation)
- [ ] Supports limit parameter for context window
- [ ] Returns empty list if no messages exist
- [ ] Function documented with docstring

**References:**
- Specification: Conversation Behavior - Context Awareness
- Plan: Conversation History Handling, Stateless Design

**Validation:**
- Unit test: Retrieve messages for user
- Unit test: Verify chronological order
- Unit test: Verify user isolation (no cross-user retrieval)
- Unit test: Verify limit parameter works

---

### Task 1.5: Implement Tool Call Record Storage Functions
**Component:** Persistence Layer
**Prerequisite:** Task 1.4
**Description:** Implement functions to store tool call records linked to conversation messages.

**Acceptance Criteria:**
- [ ] Function: store_tool_call(message_id, tool_name, parameters, result, status) → tool_call_id
- [ ] Generates unique tool call ID
- [ ] Stores tool call with timestamp
- [ ] Links to message_id
- [ ] Stores parameters and result as structured data
- [ ] Atomic write operation
- [ ] Function documented with docstring

**References:**
- Specification: Data Requirements - Tool Call Records
- Plan: Persistence Strategy, Stateless Design

**Validation:**
- Unit test: Store tool call and verify retrieval
- Unit test: Verify linkage to message
- Unit test: Verify structured data preservation

---

### Task 1.6: Test Persistence Layer Extensions
**Component:** Persistence Layer
**Prerequisite:** Task 1.5
**Description:** Comprehensive integration testing of conversation persistence functions.

**Acceptance Criteria:**
- [ ] Integration test: Store and retrieve multi-turn conversation
- [ ] Integration test: Store messages and tool calls, verify linkage
- [ ] Integration test: Verify user data isolation across multiple users
- [ ] Integration test: Verify conversation survives application restart
- [ ] All tests pass successfully

**References:**
- Plan: Stateless Design - Reproducibility
- Constitution: Deterministic Behavior

**Validation:**
- All persistence tests pass
- Data integrity verified
- User isolation verified

---

## PHASE 2: MCP Server Implementation

### Task 2.1: Initialize MCP Server with Official SDK
**Component:** MCP Server
**Prerequisite:** Task 1.6
**Description:** Set up MCP Server using Official MCP SDK and configure basic structure.

**Acceptance Criteria:**
- [ ] MCP Server initialized with Official MCP SDK
- [ ] Server can start and stop cleanly
- [ ] Basic health check endpoint works
- [ ] Logging configured
- [ ] Server is stateless (verified in code review)

**References:**
- Plan: MCP Server Responsibilities
- Constitution: Mandatory Core Stack - MCP SDK

**Validation:**
- Server starts without errors
- Health check returns success
- Code review confirms stateless design

---

### Task 2.2: Implement Create Todo MCP Tool
**Component:** MCP Server
**Prerequisite:** Task 2.1
**Description:** Define and implement the create_todo tool for MCP Server.

**Acceptance Criteria:**
- [ ] Tool schema defined: name="create_todo", parameters=(title, description, user_id)
- [ ] Tool description written for agent understanding
- [ ] Tool validates required parameters (title, user_id)
- [ ] Tool applies Phase II business logic validation
- [ ] Tool calls persistence layer to create todo
- [ ] Tool returns structured result with created todo
- [ ] Tool handles errors and returns error responses
- [ ] Tool enforces user_id authorization

**References:**
- Specification: Capability 1 - Add a Todo via Natural Language
- Plan: MCP Design - Tool 1: Create Todo Tool

**Validation:**
- Unit test: Call tool with valid parameters → success
- Unit test: Call tool with missing title → validation error
- Unit test: Verify todo created in persistence
- Unit test: Verify user_id isolation

---

### Task 2.3: Implement List Todos MCP Tool
**Component:** MCP Server
**Prerequisite:** Task 2.2
**Description:** Define and implement the list_todos tool for MCP Server.

**Acceptance Criteria:**
- [ ] Tool schema defined: name="list_todos", parameters=(user_id, status, limit)
- [ ] Tool description written for agent understanding
- [ ] Tool validates user_id parameter
- [ ] Tool calls persistence layer to retrieve todos
- [ ] Tool supports optional status filtering
- [ ] Tool supports limit parameter
- [ ] Tool returns array of todo objects
- [ ] Tool handles empty list gracefully
- [ ] Tool enforces user_id isolation

**References:**
- Specification: Capability 2 - List Todos via Chat
- Plan: MCP Design - Tool 2: List Todos Tool

**Validation:**
- Unit test: Call tool for user with todos → returns list
- Unit test: Call tool for user with no todos → returns empty array
- Unit test: Verify status filtering works
- Unit test: Verify user_id isolation (no cross-user data)

---

### Task 2.4: Implement Update Todo MCP Tool
**Component:** MCP Server
**Prerequisite:** Task 2.3
**Description:** Define and implement the update_todo tool for MCP Server.

**Acceptance Criteria:**
- [ ] Tool schema defined: name="update_todo", parameters=(todo_id, user_id, title, description, status)
- [ ] Tool description written for agent understanding
- [ ] Tool validates required parameters (todo_id, user_id)
- [ ] Tool verifies todo ownership (user_id matches)
- [ ] Tool applies Phase II validation rules
- [ ] Tool calls persistence layer to update todo
- [ ] Tool returns updated todo object
- [ ] Tool handles not found errors
- [ ] Tool handles unauthorized access errors

**References:**
- Specification: Capability 3 - Update a Todo via Chat
- Plan: MCP Design - Tool 3: Update Todo Tool

**Validation:**
- Unit test: Call tool with valid update → success
- Unit test: Call tool for non-existent todo → not found error
- Unit test: Call tool with wrong user_id → unauthorized error
- Unit test: Verify todo updated in persistence

---

### Task 2.5: Implement Complete Todo MCP Tool
**Component:** MCP Server
**Prerequisite:** Task 2.4
**Description:** Define and implement the complete_todo tool for MCP Server.

**Acceptance Criteria:**
- [ ] Tool schema defined: name="complete_todo", parameters=(todo_id, user_id)
- [ ] Tool description written for agent understanding
- [ ] Tool validates required parameters
- [ ] Tool verifies todo ownership
- [ ] Tool updates todo status to completed
- [ ] Tool updates updated_at timestamp
- [ ] Tool returns updated todo object
- [ ] Tool handles errors (not found, unauthorized, already completed)

**References:**
- Specification: Capability 4 - Mark a Todo as Complete via Chat
- Plan: MCP Design - Tool 4: Complete Todo Tool

**Validation:**
- Unit test: Call tool for pending todo → status changed to completed
- Unit test: Call tool for already completed todo → appropriate response
- Unit test: Call tool with wrong user_id → unauthorized error
- Unit test: Verify status updated in persistence

---

### Task 2.6: Implement Delete Todo MCP Tool
**Component:** MCP Server
**Prerequisite:** Task 2.5
**Description:** Define and implement the delete_todo tool for MCP Server.

**Acceptance Criteria:**
- [ ] Tool schema defined: name="delete_todo", parameters=(todo_id, user_id)
- [ ] Tool description written for agent understanding (mentions permanent deletion)
- [ ] Tool validates required parameters
- [ ] Tool verifies todo ownership
- [ ] Tool calls persistence layer to delete todo
- [ ] Tool returns confirmation message
- [ ] Tool handles errors (not found, unauthorized)

**References:**
- Specification: Capability 5 - Delete a Todo via Chat
- Plan: MCP Design - Tool 5: Delete Todo Tool

**Validation:**
- Unit test: Call tool for existing todo → todo deleted
- Unit test: Verify todo removed from persistence
- Unit test: Call tool with wrong user_id → unauthorized error
- Unit test: Call tool for non-existent todo → not found error

---

### Task 2.7: Register All Tools with MCP Server
**Component:** MCP Server
**Prerequisite:** Task 2.6
**Description:** Register all implemented tools with MCP SDK and expose them for agent invocation.

**Acceptance Criteria:**
- [ ] All 5 tools registered with MCP SDK
- [ ] Tool schemas exported for agent configuration
- [ ] Tool descriptions are clear and agent-friendly
- [ ] MCP Server can list all available tools
- [ ] Tool invocation routing works correctly

**References:**
- Plan: MCP Server Responsibilities - Tool Definition
- Constitution: Tooling Layer Requirements

**Validation:**
- Query MCP Server for tool list → returns 5 tools
- Verify tool schemas are correct
- Test tool invocation routing

---

### Task 2.8: Test MCP Server End-to-End
**Component:** MCP Server
**Prerequisite:** Task 2.7
**Description:** Comprehensive integration testing of MCP Server with all tools.

**Acceptance Criteria:**
- [ ] Integration test: Create, list, update, complete, delete todo flow
- [ ] Integration test: Multi-user isolation (2 users with separate todos)
- [ ] Integration test: Error scenarios (not found, unauthorized, validation)
- [ ] Integration test: Verify stateless behavior (restart server, data persists)
- [ ] All tests pass successfully

**References:**
- Plan: MCP Server Responsibilities
- Constitution: Stateless Architecture, Deterministic Behavior

**Validation:**
- All MCP Server tests pass
- Tool operations verified end-to-end
- User isolation confirmed

---

## PHASE 3: OpenAI Agent Configuration

### Task 3.1: Initialize OpenAI Agent with Agents SDK
**Component:** OpenAI Agent
**Prerequisite:** Task 2.8
**Description:** Set up OpenAI Agent using Agents SDK and configure basic parameters.

**Acceptance Criteria:**
- [ ] Agent initialized with OpenAI Agents SDK
- [ ] Agent configured with appropriate model (e.g., GPT-4)
- [ ] API keys configured securely
- [ ] Agent logging enabled
- [ ] Basic agent invocation works (simple prompt/response)

**References:**
- Plan: OpenAI Agent Responsibilities
- Constitution: Mandatory Core Stack - OpenAI Agents SDK

**Validation:**
- Agent responds to test prompt
- API connection verified
- Logging captures agent activity

---

### Task 3.2: Configure Agent with MCP Tool Definitions
**Component:** OpenAI Agent
**Prerequisite:** Task 3.1
**Description:** Load MCP tool schemas into agent configuration so agent can invoke tools.

**Acceptance Criteria:**
- [ ] Agent configured with all 5 MCP tool schemas
- [ ] Tool descriptions passed to agent
- [ ] Agent understands tool parameters
- [ ] Agent can invoke tools via Agents SDK tool calling mechanism
- [ ] Tool invocation routing to MCP Server configured

**References:**
- Plan: Agent Configuration Strategy, MCP Design
- Constitution: Tool Interaction Requirements

**Validation:**
- Query agent for available tools → returns 5 tools
- Test agent tool call → successfully routes to MCP Server
- Verify tool parameters passed correctly

---

### Task 3.3: Configure Agent System Prompt for Todo Management
**Component:** OpenAI Agent
**Prerequisite:** Task 3.2
**Description:** Define and configure agent system prompt to guide conversational behavior.

**Acceptance Criteria:**
- [ ] System prompt instructs agent to help with todo management
- [ ] Prompt emphasizes natural language conversation
- [ ] Prompt instructs agent to use tools for all data operations
- [ ] Prompt instructs agent to confirm destructive actions (delete)
- [ ] Prompt instructs agent to ask clarifying questions when needed
- [ ] Prompt emphasizes friendly, helpful tone
- [ ] Prompt documented in code

**References:**
- Specification: Agent Behavior Specification
- Plan: Agent Responsibilities

**Validation:**
- Review system prompt against specification
- Test agent behavior with sample prompts
- Verify conversational tone

---

### Task 3.4: Implement Agent Intent Recognition for Create Todo
**Component:** OpenAI Agent
**Prerequisite:** Task 3.3
**Description:** Verify agent correctly recognizes create todo intent and invokes create_todo tool.

**Acceptance Criteria:**
- [ ] Agent recognizes "Add task to X" → invokes create_todo(title="X")
- [ ] Agent recognizes "Create todo: X" → invokes create_todo
- [ ] Agent recognizes "Remind me to X" → invokes create_todo
- [ ] Agent recognizes "I need to X" → invokes create_todo
- [ ] Agent extracts title from various phrasings
- [ ] Agent asks for title if not provided
- [ ] Agent responds with confirmation after tool success

**References:**
- Specification: Capability 1 - Add a Todo, Agent Behavior - Intent Understanding
- Plan: Agent Responsibilities - Intent Understanding

**Validation:**
- Test: "Add a task to buy groceries" → tool called with title="Buy groceries"
- Test: "Add a task" → agent asks "What would you like to add?"
- Test: Multiple phrasings → same intent recognized

---

### Task 3.5: Implement Agent Intent Recognition for List Todos
**Component:** OpenAI Agent
**Prerequisite:** Task 3.4
**Description:** Verify agent correctly recognizes list todos intent and invokes list_todos tool.

**Acceptance Criteria:**
- [ ] Agent recognizes "Show my tasks" → invokes list_todos
- [ ] Agent recognizes "What's on my list?" → invokes list_todos
- [ ] Agent recognizes "List my todos" → invokes list_todos
- [ ] Agent recognizes "What do I need to do?" → invokes list_todos
- [ ] Agent formats tool result into readable list
- [ ] Agent handles empty list gracefully
- [ ] Agent responds naturally with todo list

**References:**
- Specification: Capability 2 - List Todos, Agent Behavior - Response Clarity
- Plan: Agent Responsibilities - Response Generation

**Validation:**
- Test: "Show me my tasks" → tool called → formatted list returned
- Test: "What do I need to do?" → same tool called
- Test: Empty list → agent responds "You don't have any todos yet"

---

### Task 3.6: Implement Agent Intent Recognition for Update Todo
**Component:** OpenAI Agent
**Prerequisite:** Task 3.5
**Description:** Verify agent correctly recognizes update todo intent and invokes update_todo tool.

**Acceptance Criteria:**
- [ ] Agent recognizes "Change X task to Y" → invokes update_todo
- [ ] Agent recognizes "Update X task" → invokes update_todo
- [ ] Agent recognizes "Rename X to Y" → invokes update_todo
- [ ] Agent identifies which todo to update from description
- [ ] Agent asks clarification if todo reference is ambiguous
- [ ] Agent confirms update after tool success

**References:**
- Specification: Capability 3 - Update a Todo, Agent Behavior - Clarifying Questions
- Plan: Agent Responsibilities - Intent Understanding

**Validation:**
- Test: "Change the grocery task to buy vegetables" → tool called with correct todo_id and new title
- Test: "Update the task" (multiple todos exist) → agent asks which task
- Test: Agent confirms "I've updated your task..."

---

### Task 3.7: Implement Agent Intent Recognition for Complete Todo
**Component:** OpenAI Agent
**Prerequisite:** Task 3.6
**Description:** Verify agent correctly recognizes complete todo intent and invokes complete_todo tool.

**Acceptance Criteria:**
- [ ] Agent recognizes "Mark X as done" → invokes complete_todo
- [ ] Agent recognizes "Complete X" → invokes complete_todo
- [ ] Agent recognizes "I finished X" → invokes complete_todo
- [ ] Agent recognizes "Check off X" → invokes complete_todo
- [ ] Agent identifies correct todo from description
- [ ] Agent asks clarification if ambiguous
- [ ] Agent celebrates completion in response

**References:**
- Specification: Capability 4 - Mark a Todo as Complete
- Plan: Agent Responsibilities - Response Generation

**Validation:**
- Test: "Mark the grocery task as done" → tool called
- Test: "I finished X" → same intent recognized
- Test: Agent responds "Great! I've marked X as complete"

---

### Task 3.8: Implement Agent Intent Recognition for Delete Todo
**Component:** OpenAI Agent
**Prerequisite:** Task 3.7
**Description:** Verify agent correctly recognizes delete intent, asks confirmation, and invokes delete_todo tool.

**Acceptance Criteria:**
- [ ] Agent recognizes "Delete X" → asks confirmation
- [ ] Agent recognizes "Remove X" → asks confirmation
- [ ] Agent asks "Are you sure?" before deletion
- [ ] Agent only invokes delete_todo after user confirms
- [ ] Agent cancels if user says no
- [ ] Agent confirms deletion after tool success

**References:**
- Specification: Capability 5 - Delete a Todo, Agent Behavior - Confirmation of Destructive Actions
- Plan: Agent Responsibilities - Tool Orchestration

**Validation:**
- Test: "Delete X" → agent asks "Are you sure?"
- Test: User confirms "Yes" → tool called → todo deleted
- Test: User declines "No" → deletion cancelled, agent acknowledges
- Test: Agent responds "I've deleted X from your list"

---

### Task 3.9: Implement Agent Multi-Turn Conversation Context Handling
**Component:** OpenAI Agent
**Prerequisite:** Task 3.8
**Description:** Configure agent to use conversation history for context in multi-turn interactions.

**Acceptance Criteria:**
- [ ] Agent receives conversation history with each request
- [ ] Agent uses history to resolve references ("it", "that task", "the grocery one")
- [ ] Agent maintains conversational flow across turns
- [ ] Agent can follow up on previous questions
- [ ] Agent doesn't repeat information unnecessarily

**References:**
- Specification: Conversation Behavior - Multi-Turn Conversations
- Plan: Agent Responsibilities - Context Management

**Validation:**
- Test: User: "Add task X" → Agent confirms → User: "Change it to Y" → Agent updates X
- Test: User: "Show my tasks" → Agent lists → User: "Complete the first one" → Agent completes correct todo
- Test: Agent references previous context naturally

---

### Task 3.10: Test Agent End-to-End with Mock MCP Tools
**Component:** OpenAI Agent
**Prerequisite:** Task 3.9
**Description:** Comprehensive testing of agent with mock MCP tool responses.

**Acceptance Criteria:**
- [ ] Test all 5 conversational capabilities with mock tools
- [ ] Test intent recognition across various phrasings
- [ ] Test clarification question behavior
- [ ] Test confirmation behavior for delete
- [ ] Test multi-turn conversation flows
- [ ] Test error handling (tool failures, invalid intent)
- [ ] All tests pass successfully

**References:**
- Specification: Success Criteria (all capabilities)
- Plan: Agent Responsibilities

**Validation:**
- All agent tests pass with mock tools
- Agent behavior matches specification
- Conversational quality verified

---

## PHASE 4: FastAPI Chat Endpoint Implementation

### Task 4.1: Create FastAPI Chat Endpoint Route
**Component:** FastAPI Backend
**Prerequisite:** Task 3.10
**Description:** Define new HTTP endpoint for chat interactions.

**Acceptance Criteria:**
- [ ] Endpoint created: POST /api/chat
- [ ] Endpoint accepts JSON body with message content
- [ ] Endpoint protected by authentication middleware
- [ ] Endpoint extracts user_id from authenticated session
- [ ] Endpoint returns JSON response with agent message
- [ ] Endpoint handles errors gracefully

**References:**
- Plan: FastAPI Chat Endpoint Responsibilities
- Constitution: API Gateway Layer

**Validation:**
- Test authenticated request → 200 OK
- Test unauthenticated request → 401 Unauthorized
- Test endpoint accepts and returns correct format

---

### Task 4.2: Implement Conversation History Retrieval in Chat Endpoint
**Component:** FastAPI Backend
**Prerequisite:** Task 4.1
**Description:** Load recent conversation history from persistence when processing chat request.

**Acceptance Criteria:**
- [ ] Endpoint retrieves recent messages for user_id
- [ ] Retrieves last N messages (configurable, default 50)
- [ ] Messages retrieved in chronological order
- [ ] Empty history handled gracefully
- [ ] User_id isolation enforced

**References:**
- Plan: Request/Response Flow - Step 2
- Specification: Conversation Behavior - Context Awareness

**Validation:**
- Test: User with history → history retrieved
- Test: User without history → empty array
- Test: Verify user isolation (no cross-user history)

---

### Task 4.3: Implement Agent Invocation in Chat Endpoint
**Component:** FastAPI Backend
**Prerequisite:** Task 4.2
**Description:** Invoke OpenAI Agent with user message and conversation history.

**Acceptance Criteria:**
- [ ] Endpoint constructs agent request with:
  - Current user message
  - Conversation history
  - User context (user_id)
- [ ] Endpoint invokes agent via Agents SDK
- [ ] Endpoint waits for agent response
- [ ] Endpoint handles agent errors
- [ ] Agent invocation includes tool call routing to MCP Server

**References:**
- Plan: Request/Response Flow - Step 3, FastAPI Responsibilities
- Constitution: AI Reasoning Layer

**Validation:**
- Test: Send message → agent invoked → response received
- Test: Agent has access to history
- Test: Agent can invoke MCP tools

---

### Task 4.4: Implement Tool Call Routing from Agent to MCP Server
**Component:** FastAPI Backend
**Prerequisite:** Task 4.3
**Description:** Route agent tool calls to MCP Server and return results to agent.

**Acceptance Criteria:**
- [ ] Agent tool calls intercepted by FastAPI
- [ ] Tool calls routed to MCP Server
- [ ] User context (user_id) included in tool calls
- [ ] Tool results returned to agent
- [ ] Tool call errors handled and returned to agent
- [ ] Tool call records captured for storage

**References:**
- Plan: Request/Response Flow - Steps 4-7
- Constitution: Tool Execution Layer

**Validation:**
- Test: Agent invokes create_todo → MCP Server called → result returned
- Test: Tool error → error returned to agent
- Test: User_id correctly propagated

---

### Task 4.5: Implement Conversation Persistence in Chat Endpoint
**Component:** FastAPI Backend
**Prerequisite:** Task 4.4
**Description:** Store user message, agent response, and tool calls in persistence layer.

**Acceptance Criteria:**
- [ ] Store user message immediately upon receipt
- [ ] Store agent response after agent returns
- [ ] Store tool call records linked to messages
- [ ] All storage operations include user_id
- [ ] Storage happens before response returned to UI
- [ ] Storage errors handled gracefully

**References:**
- Plan: Request/Response Flow - Step 9, Stateless Design
- Specification: Data Requirements

**Validation:**
- Test: Send message → verify user message stored
- Test: Receive agent response → verify response stored
- Test: Tool calls made → verify tool calls stored
- Test: Verify all data linked correctly

---

### Task 4.6: Implement Error Handling in Chat Endpoint
**Component:** FastAPI Backend
**Prerequisite:** Task 4.5
**Description:** Handle all error scenarios and return user-friendly responses.

**Acceptance Criteria:**
- [ ] Authentication errors → 401 with message
- [ ] Agent errors → user-friendly error message
- [ ] Tool errors → handled by agent, or fallback message
- [ ] Persistence errors → logged, user notified
- [ ] Unexpected errors → generic error message
- [ ] All errors logged with details
- [ ] No internal error details exposed to user

**References:**
- Plan: Error Handling Strategy
- Specification: Error and Edge Case Specifications

**Validation:**
- Test each error scenario
- Verify user-friendly messages returned
- Verify no stack traces or internal details exposed
- Verify errors logged

---

### Task 4.7: Test FastAPI Chat Endpoint End-to-End
**Component:** FastAPI Backend
**Prerequisite:** Task 4.6
**Description:** Comprehensive integration testing of chat endpoint with agent and MCP Server.

**Acceptance Criteria:**
- [ ] Integration test: Send message → agent processes → response returned
- [ ] Integration test: Create todo via chat → todo created in persistence
- [ ] Integration test: Multi-turn conversation → context maintained
- [ ] Integration test: Authentication enforcement
- [ ] Integration test: Error scenarios (tool failure, invalid intent)
- [ ] Integration test: Conversation persistence verified
- [ ] All tests pass successfully

**References:**
- Plan: Request/Response Flow (complete end-to-end)
- Constitution: Deterministic Behavior

**Validation:**
- All chat endpoint tests pass
- End-to-end flow verified
- Stateless behavior confirmed

---

## PHASE 5: Chat UI Implementation (OpenAI ChatKit)

### Task 5.1: Set Up OpenAI ChatKit Component
**Component:** Chat UI
**Prerequisite:** Task 4.7
**Description:** Initialize OpenAI ChatKit library and create basic chat interface component.

**Acceptance Criteria:**
- [ ] OpenAI ChatKit installed and imported
- [ ] Basic chat component rendered in UI
- [ ] Chat component displays message list
- [ ] Chat component has input field
- [ ] Chat component has send button
- [ ] Component styled appropriately

**References:**
- Plan: Chat UI Responsibilities
- Constitution: Presentation Layer - OpenAI ChatKit

**Validation:**
- Chat UI renders without errors
- Basic UI elements visible and functional
- Styling matches application design

---

### Task 5.2: Implement Message Display in Chat UI
**Component:** Chat UI
**Prerequisite:** Task 5.1
**Description:** Display conversation messages with clear user/assistant distinction.

**Acceptance Criteria:**
- [ ] Messages displayed in chronological order
- [ ] User messages visually distinct from assistant messages
- [ ] Messages show timestamps
- [ ] Messages support formatted text (lists, emphasis)
- [ ] Auto-scroll to latest message
- [ ] Empty state shown if no messages

**References:**
- Plan: Chat UI Responsibilities - Message Display
- Specification: Conversational Capabilities

**Validation:**
- Test: Display mock messages → correct rendering
- Test: User vs assistant messages visually distinct
- Test: Auto-scroll works on new message

---

### Task 5.3: Implement User Input Handling in Chat UI
**Component:** Chat UI
**Prerequisite:** Task 5.2
**Description:** Capture user text input and send to FastAPI chat endpoint.

**Acceptance Criteria:**
- [ ] Input field captures user text
- [ ] Send button triggers message submission
- [ ] Enter key triggers message submission
- [ ] Empty messages rejected (validation)
- [ ] Input cleared after submission
- [ ] Loading indicator shown while waiting for response
- [ ] Message sent to POST /api/chat endpoint

**References:**
- Plan: Chat UI Responsibilities - User Input Handling
- Specification: User Experience

**Validation:**
- Test: Type message and click send → message sent to backend
- Test: Type message and press enter → message sent
- Test: Empty message → not sent
- Test: Loading indicator appears

---

### Task 5.4: Implement Conversation History Loading in Chat UI
**Component:** Chat UI
**Prerequisite:** Task 5.3
**Description:** Load and display previous conversation history when chat UI mounts.

**Acceptance Criteria:**
- [ ] On mount, fetch conversation history from FastAPI
- [ ] Display loaded messages in chat
- [ ] Handle empty history gracefully
- [ ] Show loading state while fetching
- [ ] Handle fetch errors gracefully

**References:**
- Plan: Chat UI Responsibilities - Conversation Rendering
- Specification: Conversation Behavior - Cross-Session Continuity

**Validation:**
- Test: Open chat with existing history → history displayed
- Test: Open chat with no history → empty state shown
- Test: Fetch error → error message shown

---

### Task 5.5: Implement Agent Response Streaming (Optional) or Polling
**Component:** Chat UI
**Prerequisite:** Task 5.4
**Description:** Display agent responses as they arrive (streaming if supported, else simple display).

**Acceptance Criteria:**
- [ ] Agent response displayed when received
- [ ] If streaming supported: display response as it streams
- [ ] If streaming not supported: display complete response
- [ ] Loading indicator shown while agent is processing
- [ ] Response appended to message list
- [ ] UI remains responsive during wait

**References:**
- Plan: Chat UI Responsibilities - Conversation Rendering
- Specification: User Experience

**Validation:**
- Test: Send message → wait → response appears
- Test: Loading indicator shown during wait
- Test: Response correctly formatted and displayed

---

### Task 5.6: Implement Authentication Context in Chat UI
**Component:** Chat UI
**Prerequisite:** Task 5.5
**Description:** Display authenticated user info and handle authentication state.

**Acceptance Criteria:**
- [ ] Display logged-in user name/email
- [ ] Provide logout functionality
- [ ] Handle session expiration (redirect to login)
- [ ] Include authentication token in API requests
- [ ] Handle 401 errors gracefully

**References:**
- Plan: Chat UI Responsibilities - Session Management UI
- Constitution: Authentication Requirements

**Validation:**
- Test: Logged in user → name displayed
- Test: Logout → redirect to login page
- Test: Session expired → redirect to login
- Test: 401 error → appropriate handling

---

### Task 5.7: Test Chat UI End-to-End with Backend
**Component:** Chat UI
**Prerequisite:** Task 5.6
**Description:** Comprehensive testing of chat UI with live FastAPI backend.

**Acceptance Criteria:**
- [ ] Integration test: Send message → receive response → display
- [ ] Integration test: Multi-turn conversation in UI
- [ ] Integration test: Load history on mount
- [ ] Integration test: Create, list, update, complete, delete todos via chat
- [ ] Integration test: Authentication flow
- [ ] Integration test: Error scenarios
- [ ] All tests pass successfully

**References:**
- Specification: Success Criteria (all capabilities)
- Plan: High-Level System Architecture (complete stack)

**Validation:**
- All chat UI tests pass
- Full stack integration verified
- User experience validated

---

## PHASE 6: Integration and End-to-End Testing

### Task 6.1: Test Complete Todo Management Flow via Chat
**Component:** Full Stack
**Prerequisite:** Task 5.7
**Description:** Test all five conversational capabilities end-to-end with full stack.

**Acceptance Criteria:**
- [ ] Test: Add todo via chat → todo created and visible
- [ ] Test: List todos via chat → correct list displayed
- [ ] Test: Update todo via chat → todo updated
- [ ] Test: Complete todo via chat → status changed
- [ ] Test: Delete todo via chat (with confirmation) → todo deleted
- [ ] All operations verified in persistence
- [ ] Conversation history persisted correctly

**References:**
- Specification: Success Criteria - All Capabilities
- Plan: Request/Response Flow (complete)

**Validation:**
- All five capabilities work end-to-end
- Data persistence verified
- Conversation history verified

---

### Task 6.2: Test Multi-Turn Conversation Flows
**Component:** Full Stack
**Prerequisite:** Task 6.1
**Description:** Test complex multi-turn conversations with context and references.

**Acceptance Criteria:**
- [ ] Test: Create todo → reference it as "that task" → update works
- [ ] Test: List todos → reference "the first one" → complete works
- [ ] Test: Ambiguous reference → agent asks clarification → user clarifies → operation succeeds
- [ ] Test: Delete todo → agent asks confirmation → user confirms → deleted
- [ ] Test: Agent uses conversation context correctly

**References:**
- Specification: Success Criteria - Multi-Turn Conversation
- Plan: Multi-Turn Conversation Flow

**Validation:**
- Multi-turn flows work correctly
- Context resolution verified
- Agent behavior matches specification

---

### Task 6.3: Test Cross-Session Conversation Continuity
**Component:** Full Stack
**Prerequisite:** Task 6.2
**Description:** Test conversation history preservation across sessions.

**Acceptance Criteria:**
- [ ] Test: Session 1: Create 3 todos → close chat
- [ ] Test: Session 2: Open chat → history visible → list todos → 3 todos shown
- [ ] Test: Session 2: Reference previous conversation → agent recalls context
- [ ] Test: Conversation history persisted correctly
- [ ] Test: Application restart → history still accessible

**References:**
- Specification: Success Criteria - Context Awareness from History
- Plan: Stateless Design - Cross-Session Continuity

**Validation:**
- History preserved across sessions
- Application restart doesn't lose data
- Context continuity verified

---

### Task 6.4: Test User Data Isolation and Security
**Component:** Full Stack
**Prerequisite:** Task 6.3
**Description:** Test multi-user scenarios and verify data isolation.

**Acceptance Criteria:**
- [ ] Test: User A creates todos → User B cannot see them
- [ ] Test: User A's conversation history not visible to User B
- [ ] Test: User A cannot update/delete User B's todos
- [ ] Test: Unauthenticated access rejected
- [ ] Test: Session expiration handled correctly
- [ ] Test: Authentication context propagated correctly

**References:**
- Plan: Security Considerations - User Data Isolation
- Constitution: Authentication and Authorization

**Validation:**
- User isolation verified
- Security boundaries enforced
- Authentication working correctly

---

### Task 6.5: Test Error Handling Across Full Stack
**Component:** Full Stack
**Prerequisite:** Task 6.4
**Description:** Test all error scenarios end-to-end.

**Acceptance Criteria:**
- [ ] Test: Invalid user input → agent asks clarification
- [ ] Test: Tool failure (simulate) → user-friendly error message
- [ ] Test: Non-existent todo reference → agent informs user
- [ ] Test: Unauthorized access → rejected appropriately
- [ ] Test: Persistence error → handled gracefully
- [ ] Test: No errors expose internal details

**References:**
- Specification: Success Criteria - Error Handling
- Plan: Error Handling Strategy

**Validation:**
- All error scenarios handled correctly
- User-friendly error messages verified
- No internal details exposed

---

### Task 6.6: Test Stateless Architecture and Reproducibility
**Component:** Full Stack
**Prerequisite:** Task 6.5
**Description:** Verify system maintains no runtime state and behavior is deterministic.

**Acceptance Criteria:**
- [ ] Test: Same conversation history + same input → same tool calls
- [ ] Test: Restart agent/MCP/FastAPI → system state unchanged (data persists)
- [ ] Test: No in-memory state detected in agent or MCP (code review)
- [ ] Test: Conversation replay produces identical behavior
- [ ] Test: Tool call records enable reproducibility

**References:**
- Plan: Stateless Design - Statelessness Guarantees
- Constitution: Deterministic Behavior (Judge Evaluation Requirement)

**Validation:**
- Statelessness verified via code review
- Reproducibility tested and confirmed
- No hidden state detected

---

### Task 6.7: Test Phase II Compatibility and Coexistence
**Component:** Full Stack
**Prerequisite:** Task 6.6
**Description:** Verify Phase II functionality remains operational alongside Phase III.

**Acceptance Criteria:**
- [ ] Test: Phase II REST endpoints still work
- [ ] Test: Todo created via Phase II visible in Phase III chat
- [ ] Test: Todo created via Phase III chat visible in Phase II
- [ ] Test: Both interfaces access same data
- [ ] Test: Authentication shared between Phase II and III
- [ ] Test: No Phase II functionality broken by Phase III

**References:**
- Plan: Phase II Integration Strategy
- Constitution: Integration with Phase II

**Validation:**
- Phase II still functional
- Data compatibility verified
- No regressions introduced

---

### Task 6.8: Performance and Load Testing (Optional but Recommended)
**Component:** Full Stack
**Prerequisite:** Task 6.7
**Description:** Test system performance under load and concurrent users.

**Acceptance Criteria:**
- [ ] Test: Single user sends 50 messages → acceptable response time
- [ ] Test: 10 concurrent users → system remains responsive
- [ ] Test: Large conversation history (100+ messages) → performance acceptable
- [ ] Test: Database query performance adequate
- [ ] Identify any performance bottlenecks

**References:**
- Plan: Scalability considerations
- Constitution: Stateless architecture enables scaling

**Validation:**
- Performance benchmarks recorded
- No critical bottlenecks identified
- System performs acceptably

---

## PHASE 7: Documentation and Deployment Preparation

### Task 7.1: Document API Endpoints and Interfaces
**Component:** Documentation
**Prerequisite:** Task 6.8
**Description:** Create API documentation for Phase III endpoints.

**Acceptance Criteria:**
- [ ] Document POST /api/chat endpoint (request/response format)
- [ ] Document authentication requirements
- [ ] Document error response formats
- [ ] Document conversation history retrieval (if separate endpoint)
- [ ] API documentation accessible to developers

**References:**
- Plan: FastAPI Chat Endpoint
- Constitution: Spec-Driven Development

**Validation:**
- API documentation complete and accurate
- Examples provided
- Documentation reviewed

---

### Task 7.2: Document MCP Tools for Agent Configuration
**Component:** Documentation
**Prerequisite:** Task 7.1
**Description:** Document all MCP tools, schemas, and usage for agent configuration.

**Acceptance Criteria:**
- [ ] Document all 5 MCP tools with schemas
- [ ] Document tool parameters and return formats
- [ ] Document error codes and meanings
- [ ] Document tool usage guidelines
- [ ] Documentation includes examples

**References:**
- Plan: MCP Design
- Constitution: Tool Execution Layer

**Validation:**
- MCP tool documentation complete
- Schemas documented accurately
- Examples clear and helpful

---

### Task 7.3: Create User Guide for Chat Interface
**Component:** Documentation
**Prerequisite:** Task 7.2
**Description:** Create end-user documentation for using the chat interface.

**Acceptance Criteria:**
- [ ] Document how to access chat interface
- [ ] Document how to manage todos via chat (with examples)
- [ ] Document conversation capabilities
- [ ] Document how to handle errors or issues
- [ ] User guide accessible and user-friendly

**References:**
- Specification: Conversational Capabilities
- Plan: Chat UI

**Validation:**
- User guide complete
- Examples clear and helpful
- Non-technical language used

---

### Task 7.4: Create Deployment Configuration
**Component:** Deployment
**Prerequisite:** Task 7.3
**Description:** Prepare deployment configuration for Phase III components.

**Acceptance Criteria:**
- [ ] Environment variables documented
- [ ] Dependencies listed (requirements.txt, package.json, etc.)
- [ ] Configuration files created (if needed)
- [ ] Deployment instructions documented
- [ ] Security considerations documented (API keys, secrets)

**References:**
- Plan: High-Level System Architecture
- Constitution: Mandatory Core Stack

**Validation:**
- Deployment configuration reviewed
- All dependencies captured
- Instructions clear and complete

---

### Task 7.5: Verify All Constitutional Principles Upheld
**Component:** All
**Prerequisite:** Task 7.4
**Description:** Final verification that all implementation adheres to Phase III Constitution.

**Acceptance Criteria:**
- [ ] Stateless architecture verified (code review)
- [ ] Tool-based data access verified (no direct access in agent)
- [ ] Separation of concerns verified
- [ ] Spec-driven development process followed
- [ ] Phase II integration preserved
- [ ] Deterministic behavior verified
- [ ] All mandatory requirements implemented
- [ ] Optional features clearly marked as optional

**References:**
- Constitution: All sections
- Specification: All requirements
- Plan: All components

**Validation:**
- Constitutional compliance checklist completed
- All principles upheld
- No violations detected

---

### Task 7.6: Prepare Phase III Demo and Presentation
**Component:** Documentation
**Prerequisite:** Task 7.5
**Description:** Create demo script and presentation materials for Phase III.

**Acceptance Criteria:**
- [ ] Demo script covers all 5 conversational capabilities
- [ ] Demo shows multi-turn conversations
- [ ] Demo shows error handling
- [ ] Demo shows cross-session continuity
- [ ] Presentation materials highlight architecture and compliance
- [ ] Demo environment prepared and tested

**References:**
- Specification: Success Criteria
- Plan: Complete architecture
- Constitution: Phase III objectives

**Validation:**
- Demo script tested successfully
- Demo runs smoothly
- Presentation materials complete

---

## OPTIONAL BONUS TASKS (Phase 8)

These tasks are **OPTIONAL** and should only be undertaken after core Phase III is complete and validated.

### OPTIONAL Task 8.1: Implement Multi-Language Support (Urdu)
**Component:** OpenAI Agent
**Prerequisite:** Task 7.6
**Description:** Add multi-language support including Urdu to the chatbot.

**Acceptance Criteria:**
- [ ] Language detection implemented (user input)
- [ ] Agent responds in detected language
- [ ] Urdu language support tested
- [ ] Tool calls remain language-agnostic
- [ ] Language preference storable (optional)
- [ ] Core functionality unaffected

**References:**
- Specification: OPTIONAL - Multi-Language Support
- Plan: OPTIONAL Extension Points - Multi-Language

**Validation:**
- Urdu conversation tested successfully
- Language switching works
- Core functionality still works

---

### OPTIONAL Task 8.2: Implement Voice Input/Output
**Component:** Chat UI
**Prerequisite:** Task 7.6
**Description:** Add voice command support for todo management.

**Acceptance Criteria:**
- [ ] Microphone button in UI
- [ ] Speech-to-text conversion implemented
- [ ] Text-to-speech for responses (optional)
- [ ] Voice input treated same as text
- [ ] Speech errors handled gracefully
- [ ] Core functionality unaffected

**References:**
- Specification: OPTIONAL - Voice-Based Todo Commands
- Plan: OPTIONAL Extension Points - Voice Input/Output

**Validation:**
- Voice input works correctly
- Speech converted to text accurately
- Core functionality still works

---

### OPTIONAL Task 8.3: Implement Reusable Agent Skills/Subagents
**Component:** OpenAI Agent
**Prerequisite:** Task 7.6
**Description:** Create modular agent skills for complex capabilities.

**Acceptance Criteria:**
- [ ] Subagent architecture implemented
- [ ] Example subagent: Todo summarization
- [ ] Subagents use MCP tools (no bypass)
- [ ] Subagents are stateless
- [ ] Core functionality unaffected

**References:**
- Specification: OPTIONAL - Reusable Intelligence
- Plan: OPTIONAL Extension Points - Reusable Intelligence

**Validation:**
- Subagent works correctly
- MCP tools still used exclusively
- Core functionality still works

---

## Task Execution Summary

### Total Core Tasks: 63 tasks across 7 phases
### Optional Bonus Tasks: 3 tasks (Phase 8)

### Estimated Execution Order:
1. **Phase 0:** Foundation (3 tasks) - ~1-2 hours
2. **Phase 1:** Persistence (6 tasks) - ~4-6 hours
3. **Phase 2:** MCP Server (8 tasks) - ~8-12 hours
4. **Phase 3:** Agent (10 tasks) - ~10-15 hours
5. **Phase 4:** FastAPI (7 tasks) - ~6-10 hours
6. **Phase 5:** Chat UI (7 tasks) - ~6-10 hours
7. **Phase 6:** Integration Testing (8 tasks) - ~8-12 hours
8. **Phase 7:** Documentation (6 tasks) - ~4-6 hours
9. **Phase 8:** Optional Bonuses (3 tasks) - variable

### Critical Path Dependencies:
- Persistence → MCP Server → Agent → FastAPI → Chat UI
- Each phase depends on previous phase completion
- Integration testing requires all components complete

### Parallel Execution Opportunities:
- Within Phase 2: Tool implementations (Tasks 2.2-2.6) can partially overlap
- Within Phase 3: Intent recognition tasks (3.4-3.8) can partially overlap
- Phase 5 UI can start once Phase 4 API is partially complete (after Task 4.3)

---

## Task Validation Protocol

### Per-Task Validation:
1. Read task acceptance criteria
2. Execute implementation
3. Verify each acceptance criterion
4. Run specified tests
5. Document completion
6. Proceed to next task only after validation

### Phase Validation:
1. Complete all tasks in phase
2. Run phase-level integration tests
3. Verify phase objectives met
4. Review against Specification and Plan
5. Proceed to next phase only after validation

### Final Validation:
1. All core tasks completed (Phases 0-7)
2. All acceptance criteria met
3. All tests passing
4. Constitutional compliance verified
5. Phase III objectives achieved

---

## Document Status

**Version:** 1.0
**Status:** ACTIVE
**Created:** 2026-01-06
**Governed By:**
- PHASE_III_CONSTITUTION.md (architectural principles)
- PHASE_III_SPECIFICATION.md (functional requirements - WHAT)
- PHASE_III_PLAN.md (architectural design - HOW)

**Next Step:** Begin task execution starting with Phase 0

---

## Approval and Sign-Off

This task breakdown provides atomic, ordered, testable implementation tasks for Phase III. Each task is traceable to the Plan and Specification, and upholds Constitutional principles.

**Task Breakdown Complete. Awaiting approval to begin implementation execution.**

---

**END OF PHASE III TASKS**
