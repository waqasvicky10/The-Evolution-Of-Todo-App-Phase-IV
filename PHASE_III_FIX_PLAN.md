# Phase III Finalization Plan

## Goal
Address user-reported issues in Phase III:
1.  **Speech Recognition Handling**: "a task by groceries" fails to trigger "Add" intent.
2.  **Console Logging**: "API Response: Object" is opaque.
3.  **Favicon 404**: Missing favicon.

## Proposed Changes

### 1. `phase_iii/agent/providers/mock_provider.py`
**Enhance Regex Rules:**
-   Add a rule to catch commands starting with "task" or "a task" as **ADD** intent, *unless* followed by a number (which implies Update/Delete/Complete).
-   Regex: `r"^(?:a\s+)?task\s+(?!id\b|number\b|\d)(?:to\s+|by\s+|for\s+)?(.+)"`
    - `(?!...)` negative lookahead to avoid "task 1", "task id 5".
    - Captures the content as the title.

### 2. `phase_iii/chat_ui/chat.js`
**Improve Logging:**
-   Change `console.log('API Response:', data)` to `console.log('API Response:', data.response)`.
-   Add error handling visual feedback if `data.response` implies a fallback.

### 3. `phase_iii/chat_ui/index.html`
**Fix Favicon:**
-   Check if favicon link exists. If pointing to 404, either remove it or point to a valid emoji data URI for simplicity.

## Verification Plan

### Automated Tests
-   Add a new test case in `tests/unit/test_agent_urdu.py` (or create `test_agent_robustness.py`) verifying "a task by groceries" triggers `create_todo`.

### Manual Verification
-   User to verify via Speech inputs in the UI.
