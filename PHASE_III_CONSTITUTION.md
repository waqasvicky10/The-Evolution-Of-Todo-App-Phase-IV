# PHASE III CONSTITUTION
## The Evolution of Todo App - AI-Powered Todo Chatbot

### Document Purpose
This constitution defines the immutable architectural principles, technical requirements, and operational boundaries for Phase III of "The Evolution of Todo App" hackathon project. This document serves as the foundational contract that governs all downstream specifications, plans, tasks, and implementation.

---

## Phase III Definition

**Title:** AI-Powered Todo Chatbot

**Objective:** Transform the Phase II Todo system into a conversational, AI-driven chatbot where users manage todos via natural language chat interactions.

**Core Transformation:** Move from traditional UI-based todo management to an intelligent conversational interface powered by AI agents, while maintaining architectural integrity and data persistence continuity from Phase II.

---

## Mandatory Core Stack

### 1. Chat UI Layer
- **Technology:** OpenAI ChatKit
- **Responsibility:** Provide conversational interface for user interactions
- **Requirements:**
  - Display chat messages with clear user/assistant distinction
  - Support streaming responses from AI agent
  - Handle user input submission
  - Render todo information returned by agent

### 2. AI Logic Layer
- **Technology:** Local Mock AI Agent (Regex/Keyword-based)
- **Responsibility:** Understand user intent locally and orchestrate tool calls
- **Requirements:**
  - Parse natural language todo requests
  - Determine appropriate MCP tool invocations
  - Format tool results into conversational responses
  - Handle multi-turn conversations
  - Maintain conversation context through external storage only

### 3. Tooling Layer
- **Technology:** Official MCP (Model Context Protocol) SDK
- **Responsibility:** Expose todo operations as standardized tools
- **Requirements:**
  - Define tool schemas for all todo operations
  - Act as exclusive gateway to persistence layer
  - Validate tool inputs
  - Return structured tool outputs
  - Maintain zero knowledge of AI agent implementation

### 4. Backend Layer
- **Technology:** FastAPI (extended from Phase II)
- **Responsibility:** HTTP API endpoints and business logic orchestration
- **Requirements:**
  - Expose endpoints for chat interactions
  - Route agent requests to MCP server
  - Handle authentication and session management
  - Manage conversation history persistence
  - Maintain Phase II REST endpoints for compatibility

### 5. Persistence Layer
- **Technology:** Streamlit-based storage (consistent with Phase II)
- **Responsibility:** Durable storage for todos and conversation history
- **Requirements:**
  - Store todo items with all attributes
  - Store conversation history with timestamps
  - Support concurrent access patterns
  - Provide data retrieval for MCP tools
  - Maintain data integrity across sessions

---

## Core Functional Scope (MANDATORY)

### Conversational Todo Management

All todo operations must be accessible through natural language chat:

#### 1. Create Todo
- **User Intent:** "Add a task to buy groceries"
- **Agent Action:** Invoke MCP create_todo tool
- **Result:** Confirmation message with created todo details

#### 2. List Todos
- **User Intent:** "Show me all my tasks"
- **Agent Action:** Invoke MCP list_todos tool
- **Result:** Formatted list of all todos

#### 3. Update Todo
- **User Intent:** "Change the grocery task to buy vegetables"
- **Agent Action:** Invoke MCP update_todo tool
- **Result:** Confirmation message with updated todo details

#### 4. Complete Todo
- **User Intent:** "Mark the grocery task as done"
- **Agent Action:** Invoke MCP complete_todo tool
- **Result:** Confirmation message

#### 5. Delete Todo
- **User Intent:** "Remove the grocery task"
- **Agent Action:** Invoke MCP delete_todo tool
- **Result:** Confirmation message

### Additional Core Capabilities

#### 6. Conversation History
- All chat messages must be persisted
- History must be retrievable across sessions
- Timestamps must be recorded for each message
- User and assistant messages clearly distinguished

#### 7. Intent Recognition
- Agent must understand various phrasings of todo commands
- Support for ambiguous requests with clarification prompts
- Handle multi-step operations through conversation

---

## Agent Responsibilities (Mock AI)

### Primary Duties
- **Non-Negotiable**: No external AI APIs (OpenAI, Anthropic, etc.) are permitted.
- **Logic**: The AI Reasoning Layer must be a local, mock implementation.
1. **Intent Understanding:**
   - Parse natural language user input
   - Map intent to appropriate MCP tool(s)
   - Handle ambiguous requests with clarifying questions

2. **Tool Orchestration:**
   - Invoke MCP tools with correct parameters
   - Chain multiple tool calls when needed
   - Handle tool execution errors gracefully

3. **Response Generation:**
   - Format tool results into natural language
   - Provide context-aware responses
   - Maintain conversational flow

### Absolute Prohibitions
- **NEVER directly access or manipulate stored data**
- **NEVER bypass MCP tools for data operations**
- **NEVER store conversational state in runtime memory**
- **NEVER implement hardcoded command routing**
- **NEVER cache todo data in agent scope**

---

## MCP Server Responsibilities (Official MCP SDK)

### Primary Duties
1. **Tool Exposure:**
   - Define schemas for all todo CRUD operations
   - Expose tools with clear descriptions and parameters
   - Version tool definitions for stability

2. **Data Gateway:**
   - Act as the ONLY interface to persistence layer
   - Validate all tool inputs before persistence operations
   - Return structured, predictable outputs

3. **Business Logic Enforcement:**
   - Apply Phase II todo validation rules
   - Enforce data integrity constraints
   - Handle persistence layer errors

### Absolute Prohibitions
- **NEVER implement AI reasoning or intent detection**
- **NEVER maintain conversation state**
- **NEVER expose direct database access methods**
- **NEVER return unvalidated data**

---

## Stateless Architecture (NON-NEGOTIABLE)

### Core Principle
No application state may persist in runtime memory beyond the duration of a single request-response cycle. All state must be externalized to the persistence layer.

### Implementation Requirements

#### Agent Statelessness
- No in-memory conversation buffers
- No cached user preferences
- No session variables for todo data
- All context retrieved from persistence on each interaction

#### MCP Server Statelessness
- No in-memory todo caches
- No connection pooling state (except standard DB connections)
- Each tool invocation is independent
- No cross-request state sharing

#### Conversation History Management
- Every message stored immediately upon generation
- History retrieved from persistence for context
- No reliance on session memory
- Reproducible conversation state across restarts

---

## Persistence Strategy (Streamlit-Based)

### Storage Mechanism
- **Primary Storage:** Streamlit's built-in persistence mechanisms
- **Consistency:** Same storage approach used in Phase II
- **Durability:** All data survives application restarts

### Data Models

#### Todo Item
```
{
  "id": "unique_identifier",
  "title": "string",
  "description": "string",
  "status": "pending|completed",
  "created_at": "ISO8601_timestamp",
  "updated_at": "ISO8601_timestamp"
}
```

#### Conversation Message
```
{
  "id": "unique_identifier",
  "role": "user|assistant",
  "content": "string",
  "timestamp": "ISO8601_timestamp",
  "tool_calls": [optional array of tool invocations]
}
```

### Persistence Requirements
- Atomic writes for todo operations
- Append-only conversation history
- Timestamp accuracy to milliseconds
- Support for concurrent read access
- Data integrity validation on write

---

## Separation of Concerns (NON-NEGOTIABLE)

### Layer 1: Agent Reasoning (Anthropic SDK)
- **Concern:** Understanding user intent and generating responses
- **Boundaries:** No data access, no persistence, no business logic
- **Interface:** Receives user input, invokes MCP tools, returns responses

### Layer 2: Tool Execution (MCP SDK)
- **Concern:** Exposing todo operations as callable tools
- **Boundaries:** No AI logic, no UI rendering, no direct user interaction
- **Interface:** Receives tool calls, executes persistence operations, returns results

### Layer 3: Data Persistence (Streamlit Storage)
- **Concern:** Durable storage and retrieval of todos and history
- **Boundaries:** No business logic, no agent knowledge, no UI concerns
- **Interface:** CRUD operations via MCP server only

### Cross-Cutting Concerns
- **Logging:** All layers log to centralized system
- **Error Handling:** Each layer handles its own errors
- **Security:** Authentication handled at API gateway (FastAPI)

---

## Development Methodology (IMMUTABLE)

### Spec-Driven Development Process

#### Phase 1: Specification
- Define WHAT will be built
- Document all requirements
- Specify acceptance criteria
- No implementation details

#### Phase 2: Planning
- Define HOW it will be built
- Break down into components
- Identify dependencies
- Estimate complexity (not time)

#### Phase 3: Task Definition
- Create atomic, actionable tasks
- Define task inputs and outputs
- Specify validation criteria
- Assign clear ownership

#### Phase 4: Implementation
- Execute tasks only as defined
- No deviation from task specification
- No creative additions
- Validation at each task completion

### Prohibited Practices
- **NEVER code without approved tasks**
- **NEVER skip specification phase**
- **NEVER combine specification and implementation**
- **NEVER implement features not in specification**
- **NEVER deviate from architectural principles**

---

## Integration with Phase II (MANDATORY)

### Continuity Requirements
1. **Data Compatibility:**
   - Phase III must read Phase II todo data
   - No migration scripts required
   - Same data schema maintained

2. **Coexistence:**
   - Phase II REST endpoints remain functional
   - Chat interface is additive, not replacement
   - Both interfaces operate on same data

3. **Business Logic Reuse:**
   - Phase II validation rules preserved
   - Phase II error handling patterns maintained
   - No duplication of business logic

### Prohibited Actions
- **NEVER bypass Phase II persistence layer**
- **NEVER create parallel data storage**
- **NEVER modify Phase II data structures**
- **NEVER remove Phase II functionality**

---

## Deterministic Behavior (JUDGE EVALUATION REQUIREMENT)

### Reproducibility Requirements
1. **Same Input, Same Output:**
   - Given identical conversation history and user input
   - System must produce identical tool invocations
   - Results must be deterministic

2. **State Reconstruction:**
   - Application state fully reconstructable from persistence
   - No hidden state in memory
   - Restart produces identical behavior

3. **Tool Invocation Predictability:**
   - Agent must select same tools for same intents
   - Tool parameters must be deterministically derived
   - No randomness in tool selection logic

### Testing Requirements
- Integration tests must be repeatable
- Mock MCP responses for agent testing
- Persistence layer must support test fixtures
- Conversation replay capability required

---

## Explicit Exclusions from Core Scope

### What Phase III Is NOT

1. **NOT a Traditional CRUD UI:**
   - No form-based todo creation
   - No table-based todo listing
   - No direct edit interfaces

2. **NOT AI Without MCP:**
   - Agent must not directly access data
   - All persistence through tools only
   - No hardcoded data operations

3. **NOT Command-Driven:**
   - No slash commands (e.g., `/create`, `/list`)
   - No regex-based intent parsing
   - Natural language only

4. **NOT Monolithic:**
   - Agent and MCP server are separate processes
   - FastAPI orchestrates, doesn't implement
   - Clear service boundaries

5. **NOT Stateful in Memory:**
   - No session-based conversation memory
   - No in-memory caches
   - No runtime state preservation

---

## Bonus / Optional Features (CLEARLY OPTIONAL)

### Category 1: Reusable Intelligence
**Feature:** Claude Code Subagents and Agent Skills
- **Description:** Modular AI capabilities for complex todo operations
- **Optional Because:** Core functionality works without it
- **Requirements if Implemented:**
  - Must not bypass MCP tools
  - Must maintain stateless architecture
  - Must be independently testable

### Category 2: Cloud-Native Blueprints
**Feature:** Deployment automation via Agent Skills
- **Description:** Automated deployment to cloud platforms
- **Optional Because:** Local deployment sufficient for core
- **Requirements if Implemented:**
  - Must not modify core architecture
  - Must document deployment process
  - Must be reversible

### Category 3: Multi-Language Support
**Feature:** Chatbot conversations in multiple languages (including Urdu)
- **Description:** Natural language todo management in non-English languages
- **Optional Because:** English sufficient for core evaluation
- **Requirements if Implemented:**
  - Must maintain same MCP tool interfaces
  - Must handle language detection
  - Must persist language preference

### Category 4: Voice Interface
**Feature:** Voice commands for todo operations
- **Description:** Speech-to-text and text-to-speech integration
- **Optional Because:** Text chat sufficient for core
- **Requirements if Implemented:**
  - Must convert voice to text before agent processing
  - Must use same conversational flow
  - Must handle voice recognition errors

### Rules for All Bonus Features
1. **Clearly Labeled:** Must be documented as OPTIONAL
2. **Non-Blocking:** Core Phase III must function fully without them
3. **Architecture Compliant:** Must follow all constitutional principles
4. **No Shortcuts:** Cannot bypass MCP tools or persistence layer
5. **Testable:** Must include independent test cases
6. **Documented:** Must have clear implementation documentation

---

## Success Criteria

### Phase III is Successfully Completed When:

#### Functional Criteria
✓ Users can create todos through natural language chat
✓ Users can list all todos through chat
✓ Users can update specific todos through chat
✓ Users can mark todos complete through chat
✓ Users can delete todos through chat
✓ Conversation history is preserved across sessions
✓ Agent correctly interprets various phrasings of intents

#### Architectural Criteria
✓ Agent never directly accesses persistence layer
✓ All data operations go through MCP tools
✓ No runtime state persists beyond request cycle
✓ Application behavior is fully deterministic
✓ System state is reconstructable from persistence
✓ Clear separation between agent, tools, and storage

#### Integration Criteria
✓ Phase II data is accessible through Phase III
✓ Phase II REST endpoints remain functional
✓ No duplication of business logic
✓ Same Streamlit storage mechanism used

#### Quality Criteria
✓ All constitutional principles adhered to
✓ Specification-driven development followed
✓ Code is documented and testable
✓ Error handling is comprehensive
✓ Judge evaluation can reproduce behavior

---

## Constitutional Amendment Process

### This Constitution May Only Be Amended When:
1. **Hackathon Requirements Change:**
   - Official Phase III requirements are updated
   - New mandatory technologies are specified

2. **Technical Impossibility Discovered:**
   - Specified stack cannot achieve core functionality
   - Documented proof of technical limitation provided

3. **Security Vulnerability Identified:**
   - Constitutional requirement creates security risk
   - Alternative approach maintains architectural integrity

### Amendment Procedure:
1. Document proposed change and justification
2. Demonstrate alignment with hackathon objectives
3. Update PHASE_III_CONSTITUTION.md
4. Cascade changes to specification and plans
5. Re-validate all affected tasks

### Prohibited Amendments:
- **NEVER weaken separation of concerns**
- **NEVER allow stateful architecture**
- **NEVER permit direct data access by agent**
- **NEVER bypass MCP tool layer**
- **NEVER skip specification phases**

---

## Document Status

**Version:** 1.0
**Status:** ACTIVE
**Created:** 2026-01-06
**Authority:** Governs all Phase III development
**Supersedes:** None (foundational document)
**Next Document:** PHASE_III_SPECIFICATION.md (awaiting creation)

---

## Acknowledgment Declaration

By proceeding with Phase III development, all contributors acknowledge:

1. This constitution is the supreme governing document
2. All specifications must align with constitutional principles
3. All implementation must follow spec-driven methodology
4. No deviation from core architectural requirements is permitted
5. Bonus features are optional and must not compromise core
6. Judge evaluation will assess constitutional compliance

---

**END OF PHASE III CONSTITUTION**

*No specification, no plan, no tasks, and no code may be created until this constitution is approved.*
