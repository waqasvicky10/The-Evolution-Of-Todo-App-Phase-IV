# PHASE II SPECIFICATION - FULL-STACK WEB APPLICATION

**Project:** Evolution of Todo
**Phase:** II - Full-Stack Web Application
**Version:** 1.0
**Status:** DRAFT
**Constitutional Compliance:** Verified against CONSTITUTION.md v2.0
**Date:** 2026-01-01

---

## EXECUTIVE SUMMARY

Phase II transforms the Phase I in-memory console application into a production-ready, multi-user web application with persistent storage. Users will be able to register accounts, log in securely, and manage their personal todo lists through a web browser. Each user's tasks are isolated and accessible only to them. All data persists in a cloud database.

---

## CONSTITUTIONAL COMPLIANCE

This specification is created under:
- **Article I:** Spec-Driven Development Mandate
- **Article III:** Phase Governance (Section 3.1 - Phase Scope Boundaries)
- **Article IV:** Technology Constraints (Section 4.1 - Phase II Stack)
- **Article VIII:** Phase-Specific Provisions (Section 8.2 - Phase II)
- **Article IX:** Security Requirements (Authentication, Authorization, Data Protection)

All implementation must follow: Constitution → This Spec → Plan → Tasks → Code

**Technology Stack (from Constitution):**
- Frontend: Next.js (App Router) with TypeScript
- Backend: FastAPI with SQLModel ORM
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT

---

## PHASE II SCOPE

### What We Are Building

A multi-user web application where:
- Users register accounts with email and password
- Users log in to access their personal todo lists
- Each user can create, view, update, delete, and mark tasks as complete
- Users can only see and manage their own tasks
- All data persists in a database across sessions
- The application is accessible through a web browser on desktop and mobile

### What We Are NOT Building

**Explicitly Out of Scope (Phase III and beyond):**
- ❌ AI agents
- ❌ Natural language processing
- ❌ Multi-agent orchestration
- ❌ Model Context Protocol (MCP)
- ❌ Chatbot or conversational interfaces
- ❌ Intelligent task suggestions

**Also Out of Scope:**
- ❌ Advanced task features (priorities, tags, categories, due dates, subtasks)
- ❌ Real-time collaboration or task sharing between users
- ❌ File attachments
- ❌ Email or push notifications
- ❌ Social authentication (Google, GitHub, etc.)
- ❌ Admin dashboard or user management
- ❌ Task search or filtering (beyond viewing all tasks)
- ❌ Task sorting (other than default order)
- ❌ Bulk operations (select multiple tasks)

---

## USER ROLES

### Anonymous User
**Definition:** A visitor who has not registered or logged in.

**Capabilities:**
- Access landing page
- Access registration page
- Access login page

**Restrictions:**
- Cannot access dashboard
- Cannot view, create, update, or delete tasks
- Redirected to login if attempting to access protected pages

---

### Authenticated User
**Definition:** A user who has registered and logged in with valid credentials.

**Capabilities:**
- Access dashboard
- View all their own tasks
- Create new tasks
- Update their own tasks
- Delete their own tasks
- Mark their own tasks as complete or incomplete
- Log out

**Restrictions:**
- Cannot view other users' tasks
- Cannot modify other users' tasks
- Cannot delete other users' tasks
- Cannot access other users' accounts

---

## USER STORIES

### US-201: User Registration

**As a** new user
**I want to** register for an account with my email and password
**So that** I can access the todo application and manage my tasks

**Acceptance Criteria:**
1. User can navigate to a registration page
2. Registration page displays a form with fields:
   - Email address
   - Password
   - Password confirmation
3. User enters email, password, and password confirmation
4. System validates that email is a valid email format
5. System validates that email is not already registered
6. System validates that password meets minimum requirements:
   - At least 8 characters long
   - Contains at least one uppercase letter
   - Contains at least one lowercase letter
   - Contains at least one number
   - Contains at least one special character
7. System validates that password and password confirmation match
8. If all validations pass, system creates a new user account
9. Password is securely hashed before storage (never stored as plaintext)
10. User is redirected to login page with success message
11. User can then log in with their new credentials

**Error Cases:**
- **Invalid email format:** Display error "Please enter a valid email address"
- **Email already registered:** Display error "An account with this email already exists"
- **Weak password:** Display error "Password must be at least 8 characters with uppercase, lowercase, number, and special character"
- **Password mismatch:** Display error "Passwords do not match"
- **Empty fields:** Display error "All fields are required"
- **Server error:** Display error "Registration failed. Please try again later"

**Edge Cases:**
- User tries to register while already logged in: Redirect to dashboard
- User submits form multiple times: Only create account once, handle duplicate gracefully

---

### US-202: User Login

**As a** registered user
**I want to** log in with my email and password
**So that** I can access my todo list

**Acceptance Criteria:**
1. User can navigate to a login page
2. Login page displays a form with fields:
   - Email address
   - Password
3. User enters registered email and password
4. System validates credentials against database
5. If credentials are valid, system generates authentication tokens
6. User is redirected to dashboard
7. User remains logged in until they log out or tokens expire
8. If credentials are invalid, error message is displayed

**Authentication Token Behavior:**
- Access token expires after 15 minutes of inactivity
- Refresh token expires after 7 days
- When access token expires, system automatically refreshes it using refresh token
- When refresh token expires, user must log in again

**Error Cases:**
- **Invalid credentials:** Display error "Invalid email or password" (generic message for security)
- **Account not found:** Display error "Invalid email or password" (same message as above for security)
- **Empty fields:** Display error "Email and password are required"
- **Server error:** Display error "Login failed. Please try again later"

**Edge Cases:**
- User tries to log in while already logged in: Redirect to dashboard
- User enters correct email but wrong password: Show generic error (security best practice)
- User enters non-existent email: Show same generic error (security best practice)

---

### US-203: User Logout

**As a** logged-in user
**I want to** log out of my account
**So that** my session is ended and my data is secure

**Acceptance Criteria:**
1. User can click a logout button/link from any page while logged in
2. System invalidates authentication tokens
3. User is redirected to login page
4. User cannot access protected pages without logging in again
5. Attempting to access dashboard after logout redirects to login page

**Error Cases:**
- None (logout is always successful, even if tokens are already invalid)

**Edge Cases:**
- User clicks logout multiple times: Handled gracefully, no error
- User's tokens already expired: Logout still succeeds, redirect to login

---

### US-204: View Personal Task List

**As a** logged-in user
**I want to** view all my tasks in one place
**So that** I can see what I need to do

**Acceptance Criteria:**
1. User is logged in and accesses the dashboard page
2. Dashboard displays all tasks that belong to the logged-in user
3. Each task displays:
   - Task description
   - Completion status (complete or incomplete)
   - Visual indicator (checkmark for complete, empty for incomplete)
4. Tasks are displayed in a consistent order (newest first or oldest first, as specified in plan)
5. If user has no tasks, display message "No tasks yet. Create your first task!"
6. Display count of total tasks (e.g., "5 tasks")
7. Only the logged-in user's tasks are displayed (strict user isolation)

**Security Requirements:**
- User A CANNOT see User B's tasks
- All task queries must filter by the authenticated user's ID
- Attempting to access another user's tasks via URL manipulation returns error

**Error Cases:**
- **Not authenticated:** Redirect to login page
- **Invalid or expired token:** Redirect to login page
- **Server error:** Display error "Failed to load tasks. Please try again"

**Edge Cases:**
- User has zero tasks: Show empty state message
- User has hundreds of tasks: All tasks display (pagination out of scope for Phase II)

---

### US-205: Create a New Task

**As a** logged-in user
**I want to** create a new task
**So that** I can track things I need to do

**Acceptance Criteria:**
1. User is logged in and on the dashboard
2. User clicks "Add Task" button or similar action
3. System displays a form to enter task description
4. User enters task description (text input)
5. User submits the form
6. System validates task description:
   - Must not be empty
   - Must be between 1 and 500 characters
7. If valid, system creates new task in database
8. Task is associated with the logged-in user
9. Task defaults to incomplete status
10. New task appears in the user's task list immediately
11. Form closes or clears after successful creation
12. Success feedback is shown to user

**Error Cases:**
- **Empty description:** Display error "Task description cannot be empty"
- **Description too long:** Display error "Task description too long (max 500 characters)"
- **Not authenticated:** Redirect to login page
- **Invalid or expired token:** Redirect to login page
- **Server error:** Display error "Failed to create task. Please try again"

**Edge Cases:**
- User enters only whitespace: Treat as empty, show error
- User enters exactly 500 characters: Allowed
- User enters 501 characters: Show error

---

### US-206: Update a Task

**As a** logged-in user
**I want to** update a task's description
**So that** I can correct or modify task details

**Acceptance Criteria:**
1. User is logged in and viewing their task list
2. User clicks "Edit" button on a specific task
3. System displays a form pre-filled with current task description
4. User modifies the description
5. User submits the updated description
6. System validates new description:
   - Must not be empty
   - Must be between 1 and 500 characters
7. System verifies task belongs to logged-in user
8. If valid, system updates task in database
9. Updated task appears in task list with new description
10. Form closes after successful update
11. Success feedback is shown to user

**Security Requirements:**
- User can only update their own tasks
- Attempting to update another user's task returns "Access denied" error

**Error Cases:**
- **Empty description:** Display error "Task description cannot be empty"
- **Description too long:** Display error "Task description too long (max 500 characters)"
- **Task not found:** Display error "Task not found"
- **Task belongs to another user:** Display error "Access denied"
- **Not authenticated:** Redirect to login page
- **Invalid or expired token:** Redirect to login page
- **Server error:** Display error "Failed to update task. Please try again"

**Edge Cases:**
- User makes no changes and submits: Update succeeds with same description
- User edits task while another user deletes their own task: No conflict (different users)

---

### US-207: Delete a Task

**As a** logged-in user
**I want to** delete a task
**So that** I can remove tasks I no longer need

**Acceptance Criteria:**
1. User is logged in and viewing their task list
2. User clicks "Delete" button on a specific task
3. System displays confirmation dialog: "Are you sure you want to delete this task?"
4. User can confirm or cancel
5. If user confirms:
   - System verifies task belongs to logged-in user
   - System deletes task from database
   - Task is removed from task list immediately
   - Success feedback is shown to user
6. If user cancels:
   - No action is taken
   - Dialog closes

**Security Requirements:**
- User can only delete their own tasks
- Attempting to delete another user's task returns "Access denied" error

**Error Cases:**
- **Task not found:** Display error "Task not found"
- **Task belongs to another user:** Display error "Access denied"
- **Not authenticated:** Redirect to login page
- **Invalid or expired token:** Redirect to login page
- **Server error:** Display error "Failed to delete task. Please try again"

**Edge Cases:**
- User cancels deletion: Task remains unchanged
- User deletes task while another user views their own list: No conflict (different users)
- Task is already deleted (race condition): Show "Task not found" error

---

### US-208: Mark Task as Complete or Incomplete

**As a** logged-in user
**I want to** toggle a task's completion status
**So that** I can track which tasks I've finished

**Acceptance Criteria:**
1. User is logged in and viewing their task list
2. Each task displays a checkbox or toggle indicating completion status
3. User clicks checkbox/toggle for a specific task
4. System verifies task belongs to logged-in user
5. If task is incomplete, system marks it as complete
6. If task is complete, system marks it as incomplete
7. Task list updates immediately to reflect new status
8. Visual indicator changes (e.g., checkmark appears/disappears, strikethrough text)

**Security Requirements:**
- User can only toggle their own tasks
- Attempting to toggle another user's task returns "Access denied" error

**Error Cases:**
- **Task not found:** Display error "Task not found"
- **Task belongs to another user:** Display error "Access denied"
- **Not authenticated:** Redirect to login page
- **Invalid or expired token:** Redirect to login page
- **Server error:** Display error "Failed to update task. Please try again"

**Edge Cases:**
- User toggles task multiple times quickly: All requests are processed in order
- User toggles task A while another user toggles their own task B: No conflict (different users)

---

### US-209: Automatic Token Refresh

**As a** logged-in user
**I want** my session to remain active during use
**So that** I don't have to log in repeatedly

**Acceptance Criteria:**
1. User logs in successfully
2. System issues an access token (expires in 15 minutes)
3. System issues a refresh token (expires in 7 days)
4. When access token expires, system automatically uses refresh token to get new access token
5. Token refresh happens transparently (user is not interrupted)
6. If refresh token is valid, user remains logged in
7. If refresh token is expired, user is redirected to login page

**Error Cases:**
- **Refresh token expired:** Redirect to login page with message "Session expired. Please log in again"
- **Refresh token invalid:** Redirect to login page
- **Server error during refresh:** Redirect to login page

**Edge Cases:**
- User is actively using app when access token expires: Refresh happens automatically, no interruption
- User is idle for 7+ days: Refresh token expires, must log in again
- User closes browser and returns within 7 days: Still logged in (refresh token valid)

---

### US-210: Protected Route Access Control

**As a** user (authenticated or not)
**I want** the application to enforce proper access control
**So that** my data is secure and I'm directed to the appropriate pages

**Acceptance Criteria:**

**For Anonymous Users:**
1. Anonymous user can access landing page
2. Anonymous user can access registration page
3. Anonymous user can access login page
4. If anonymous user tries to access dashboard, redirect to login page

**For Authenticated Users:**
5. Authenticated user can access dashboard
6. If authenticated user tries to access login page, redirect to dashboard
7. If authenticated user tries to access registration page, redirect to dashboard
8. Authenticated user sees logout option in navigation
9. Authenticated user does NOT see login/register options in navigation

**Token Validation:**
10. System validates authentication token on every request to protected pages
11. If token is invalid or expired, redirect to login page
12. If token is valid, allow access to protected page

**Error Cases:**
- **No token present:** Redirect to login page
- **Invalid token:** Redirect to login page
- **Expired access token but valid refresh token:** Refresh token and allow access
- **Expired refresh token:** Redirect to login page with message "Session expired. Please log in again"

**Edge Cases:**
- User manipulates URL to access another user's task directly: Return "Access denied" error
- User opens multiple tabs: Authentication state consistent across tabs
- User logs out in one tab: Other tabs also lose access to protected pages

---

## AUTHENTICATION AND AUTHORIZATION BEHAVIOR

### Authentication (Who are you?)

**Registration:**
- User provides email and password
- System validates email is unique and password meets requirements
- System hashes password using bcrypt
- System stores user record in database
- User can now log in

**Login:**
- User provides email and password
- System verifies email exists in database
- System verifies password hash matches stored hash
- If valid, system generates JWT access token and refresh token
- Tokens are sent to client (stored securely)

**Token Management:**
- Access token: Short-lived (15 minutes), used for API requests
- Refresh token: Long-lived (7 days), used to get new access tokens
- Tokens contain user ID and expiration time
- Tokens are signed and cannot be tampered with

**Logout:**
- Client discards tokens
- User must log in again to access protected resources

---

### Authorization (What can you do?)

**User Data Isolation:**
- Every task belongs to exactly one user (via user_id foreign key)
- All task queries MUST filter by authenticated user's ID
- Users can ONLY perform actions on their own tasks

**Enforcement Rules:**
1. **Create Task:** Task is automatically assigned to authenticated user
2. **View Tasks:** Only tasks where `user_id = authenticated_user.id` are returned
3. **Update Task:** Only allowed if `task.user_id = authenticated_user.id`
4. **Delete Task:** Only allowed if `task.user_id = authenticated_user.id`
5. **Toggle Task:** Only allowed if `task.user_id = authenticated_user.id`

**Violation Behavior:**
- If user attempts to access another user's task: Return HTTP 403 Forbidden with message "Access denied"
- If user provides invalid token: Return HTTP 401 Unauthorized, redirect to login
- If user provides no token: Return HTTP 401 Unauthorized, redirect to login

---

## ERROR AND EDGE CASES

### Authentication Errors

| Error Condition | User Experience | System Behavior |
|----------------|----------------|-----------------|
| Invalid email format during registration | Show inline error: "Please enter a valid email address" | Do not submit form |
| Email already registered | Show error: "An account with this email already exists" | Do not create account |
| Weak password | Show error with requirements: "Password must be at least 8 characters with uppercase, lowercase, number, and special character" | Do not create account |
| Passwords don't match | Show error: "Passwords do not match" | Do not create account |
| Wrong login credentials | Show generic error: "Invalid email or password" | Do not log in, do not reveal which field is wrong |
| Expired access token | Automatically refresh using refresh token | User continues without interruption |
| Expired refresh token | Show message: "Session expired. Please log in again" | Redirect to login page |

---

### Task Operation Errors

| Error Condition | User Experience | System Behavior |
|----------------|----------------|-----------------|
| Empty task description | Show error: "Task description cannot be empty" | Do not create/update task |
| Task description >500 chars | Show error: "Task description too long (max 500 characters)" | Do not create/update task |
| Task not found | Show error: "Task not found" | Return HTTP 404 |
| Task belongs to another user | Show error: "Access denied" | Return HTTP 403 |
| Not authenticated | Redirect to login page | Return HTTP 401 |
| Server error | Show error: "Something went wrong. Please try again" | Return HTTP 500 |

---

### Authorization Errors

| Scenario | Expected Behavior |
|----------|------------------|
| User A tries to view User B's task | Return "Access denied" error |
| User A tries to update User B's task | Return "Access denied" error |
| User A tries to delete User B's task | Return "Access denied" error |
| User A tries to toggle User B's task | Return "Access denied" error |
| Anonymous user tries to access dashboard | Redirect to login page |
| Anonymous user tries to create task via API | Return HTTP 401 Unauthorized |

---

### Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| User submits registration form twice quickly | Only one account created, second request returns "Email already exists" |
| User toggles task completion rapidly | All requests processed in order, final state reflects last request |
| User deletes task that was already deleted | Return "Task not found" error |
| User edits task that was already deleted | Return "Task not found" error |
| User has zero tasks | Display empty state: "No tasks yet. Create your first task!" |
| User creates task with exactly 500 characters | Task is created successfully |
| User creates task with 501 characters | Show error: "Task description too long (max 500 characters)" |
| User enters only spaces in task description | Treat as empty, show error: "Task description cannot be empty" |
| User is logged in on multiple devices | All devices have independent sessions with their own tokens |
| User changes password (out of scope, but plan for future) | N/A - not in Phase II |

---

## DATA REQUIREMENTS

### User Data

**What we store about each user:**
- Unique identifier (auto-generated)
- Email address (unique, used for login)
- Password (hashed, never stored as plaintext)
- Account creation timestamp
- Account last updated timestamp

**Relationships:**
- One user can have many tasks
- Each task belongs to exactly one user

---

### Task Data

**What we store about each task:**
- Unique identifier (auto-generated)
- Task description (text, 1-500 characters)
- Completion status (true/false, defaults to false)
- Owner (reference to user who created it)
- Creation timestamp
- Last updated timestamp

**Relationships:**
- Each task belongs to exactly one user
- Tasks cannot be shared between users (not in Phase II scope)

---

## VALIDATION RULES

### User Registration Validation

| Field | Rules |
|-------|-------|
| Email | Required, valid email format, unique (not already registered) |
| Password | Required, minimum 8 characters, must contain uppercase, lowercase, number, special character |
| Password Confirmation | Required, must exactly match password field |

---

### Task Validation

| Field | Rules |
|-------|-------|
| Description | Required, not empty (excluding whitespace), minimum 1 character, maximum 500 characters |
| Completion Status | Boolean (true/false), defaults to false |
| User ID | Required, must reference valid user, automatically set to authenticated user |

---

### Authentication Validation

| Field | Rules |
|-------|-------|
| Access Token | Required for all protected endpoints, must be valid JWT, must not be expired (15 min lifetime) |
| Refresh Token | Required for token refresh, must be valid JWT, must not be expired (7 day lifetime) |

---

## ACCEPTANCE CRITERIA FOR PHASE II COMPLETION

Phase II is considered complete when all of the following criteria are met:

### Functional Completeness
1. ✅ Users can register new accounts with email and password
2. ✅ Users can log in with registered credentials
3. ✅ Users can log out
4. ✅ Authenticated users can view their dashboard
5. ✅ Authenticated users can see all their own tasks
6. ✅ Authenticated users can create new tasks
7. ✅ Authenticated users can update their task descriptions
8. ✅ Authenticated users can delete their tasks
9. ✅ Authenticated users can mark tasks as complete or incomplete
10. ✅ Anonymous users are redirected to login when accessing protected pages

### Security Completeness
11. ✅ Passwords are hashed (never stored as plaintext)
12. ✅ JWT authentication is enforced on all protected endpoints
13. ✅ User data isolation is enforced (users cannot access other users' tasks)
14. ✅ All task operations verify task ownership
15. ✅ Token expiration is enforced (15 min access, 7 day refresh)
16. ✅ Expired tokens redirect users to login

### Error Handling Completeness
17. ✅ All validation errors display user-friendly messages
18. ✅ All authentication errors are handled gracefully
19. ✅ All authorization errors return appropriate HTTP status codes
20. ✅ Server errors display generic "try again" messages (don't leak implementation details)

### Data Persistence Completeness
21. ✅ All user data persists in database across sessions
22. ✅ All task data persists in database across sessions
23. ✅ Users can log out, log back in, and see their tasks

### User Experience Completeness
24. ✅ Application is accessible via web browser
25. ✅ Application is responsive (works on mobile and desktop)
26. ✅ All forms validate input before submission
27. ✅ All actions provide immediate feedback (success or error)
28. ✅ Empty states are handled (no tasks, no search results, etc.)

---

## SUCCESS METRICS

Phase II will be considered successful when:

1. **All user stories are implemented** (US-201 through US-210)
2. **All acceptance criteria are met** (functional, security, error handling, data persistence, UX)
3. **Manual testing confirms**:
   - User can register, log in, and log out
   - User can perform all CRUD operations on tasks
   - User cannot access another user's tasks
   - All error cases are handled gracefully
4. **Automated testing confirms**:
   - Backend tests pass (minimum 80% coverage)
   - Frontend tests pass (minimum 70% coverage)
   - User isolation is verified
5. **Code quality standards met**:
   - Code passes linting
   - Code is formatted correctly
   - Type hints/types are present
   - No hardcoded secrets

---

## NON-GOALS (EXPLICIT EXCLUSIONS)

The following are explicitly NOT included in Phase II and must NOT be implemented:

### Phase III Features (AI/Intelligent)
- ❌ AI agents
- ❌ Natural language processing
- ❌ Multi-agent orchestration
- ❌ Model Context Protocol (MCP)
- ❌ Chatbot interfaces
- ❌ Intelligent task suggestions
- ❌ Automated task creation from context
- ❌ Agent-based task delegation

### Advanced Task Features
- ❌ Task priorities (high, medium, low)
- ❌ Task tags or categories
- ❌ Task due dates or deadlines
- ❌ Task reminders or notifications
- ❌ Subtasks or task hierarchy
- ❌ Task notes or descriptions beyond the main description field
- ❌ Task attachments (files, images)
- ❌ Task comments or activity history

### Collaboration Features
- ❌ Sharing tasks with other users
- ❌ Assigning tasks to other users
- ❌ Real-time collaboration
- ❌ Team or group features
- ❌ Task permissions (beyond owner-only)

### Advanced User Features
- ❌ User profiles (beyond email)
- ❌ User avatars
- ❌ Social authentication (Google, GitHub, etc.)
- ❌ Password reset via email
- ❌ Email verification
- ❌ Two-factor authentication
- ❌ Account deletion
- ❌ User settings or preferences

### Search and Organization
- ❌ Search functionality
- ❌ Filtering tasks (by status, date, etc.)
- ❌ Sorting tasks (beyond default order)
- ❌ Task pagination
- ❌ Bulk operations (select multiple, delete all)

### Admin and Management
- ❌ Admin dashboard
- ❌ User management (admin viewing/editing users)
- ❌ Analytics or reporting
- ❌ Audit logs

### Infrastructure (Phase IV)
- ❌ Microservices architecture
- ❌ Message queues
- ❌ Container orchestration
- ❌ Service mesh
- ❌ Advanced monitoring

---

## APPROVAL

**Specification Status:** DRAFT
**Constitutional Compliance:** VERIFIED (Constitution v2.0)
**Ready for Planning:** PENDING APPROVAL

**Next Steps:**
1. Review and approve this specification
2. Create PHASE_II_PLAN.md (implementation plan defining HOW)
3. Create PHASE_II_TASKS.md (task breakdown)
4. Begin implementation per constitutional workflow

---

**END OF PHASE II SPECIFICATION**

*This specification is subordinate to CONSTITUTION.md v2.0 and may only be amended through the constitutional amendment process defined in Article VI, Section 6.3.*
