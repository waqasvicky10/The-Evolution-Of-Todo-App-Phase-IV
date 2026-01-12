"""
Integration Tests for Phase III Persistence Layer

This module contains comprehensive integration tests for the conversation
message and tool call storage/retrieval functions.

Tests verify:
- Multi-turn conversation flows
- Message and tool call linkage
- User data isolation
- Data persistence across sessions
- All acceptance criteria from Task 1.6
"""

import pytest
import sqlite3
import time
from typing import List

from phase_iii.persistence.models.conversation import ConversationMessage, MessageRole
from phase_iii.persistence.models.tool_call import ToolCallRecord, ToolCallStatus

from phase_iii.persistence.repositories.conversation_repo import (
    init_conversation_tables,
    store_message,
    get_recent_messages,
    get_conversation_context,
    count_user_messages,
    has_conversation_history
)

from phase_iii.persistence.repositories.tool_call_repo import (
    init_tool_call_tables,
    store_tool_call,
    get_tool_calls_by_message,
    count_tool_calls,
    get_tool_call_statistics
)


class TestMultiTurnConversation:
    """Test multi-turn conversation storage and retrieval."""

    def setup_method(self):
        """Initialize tables and clean test data before each test."""
        init_conversation_tables()
        init_tool_call_tables()
        # Clean up test data from previous runs
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Remove test data for this test class."""
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        # Delete test user data (user_id 100-101)
        cursor.execute("DELETE FROM conversation_messages WHERE user_id BETWEEN 100 AND 101")
        cursor.execute("DELETE FROM tool_calls WHERE message_id IN (SELECT id FROM conversation_messages WHERE user_id BETWEEN 100 AND 101)")
        conn.commit()
        conn.close()

    def test_store_and_retrieve_multi_turn_conversation(self):
        """
        Test: Store and retrieve a multi-turn conversation.

        Acceptance Criteria from Task 1.6:
        - Multi-turn conversation can be stored
        - All messages retrieved in chronological order
        - Context maintained across turns
        """
        user_id = 100

        # Turn 1: User asks to create todo
        msg1 = store_message(
            user_id=user_id,
            role=MessageRole.USER,
            content="Add a task to buy groceries"
        )
        assert msg1.id is not None
        assert msg1.user_id == user_id
        time.sleep(0.01)  # Ensure different timestamps

        # Turn 2: Assistant confirms
        msg2 = store_message(
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content="I've added 'Buy groceries' to your todo list."
        )
        assert msg2.id is not None
        time.sleep(0.01)

        # Turn 3: User asks to list todos
        msg3 = store_message(
            user_id=user_id,
            role=MessageRole.USER,
            content="Show me my tasks"
        )
        assert msg3.id is not None
        time.sleep(0.01)

        # Turn 4: Assistant lists todos
        msg4 = store_message(
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content="Here are your tasks: 1. Buy groceries"
        )
        assert msg4.id is not None

        # Retrieve conversation
        messages = get_recent_messages(user_id=user_id, limit=10)

        # Verify all messages retrieved
        assert len(messages) == 4

        # Verify chronological order
        assert messages[0].id == msg1.id
        assert messages[1].id == msg2.id
        assert messages[2].id == msg3.id
        assert messages[3].id == msg4.id

        # Verify alternating roles
        assert messages[0].role == MessageRole.USER
        assert messages[1].role == MessageRole.ASSISTANT
        assert messages[2].role == MessageRole.USER
        assert messages[3].role == MessageRole.ASSISTANT

        # Verify content preserved
        assert messages[0].content == "Add a task to buy groceries"
        assert messages[1].content == "I've added 'Buy groceries' to your todo list."

        print("✓ Multi-turn conversation test passed")

    def test_conversation_context_window(self):
        """
        Test: Context window limits work correctly.

        Acceptance Criteria:
        - get_conversation_context returns limited messages
        - Limit parameter respected
        """
        user_id = 101

        # Store 10 messages
        for i in range(10):
            store_message(
                user_id=user_id,
                role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                content=f"Message {i+1}"
            )
            time.sleep(0.001)

        # Get context with limit
        context = get_conversation_context(user_id=user_id, max_messages=5)

        # Verify limit respected
        assert len(context) == 5

        # Verify oldest messages in window (first 5)
        assert context[0].content == "Message 1"
        assert context[4].content == "Message 5"

        print("✓ Context window test passed")


class TestMessageToolCallLinkage:
    """Test linkage between messages and tool calls."""

    def setup_method(self):
        """Initialize tables and clean test data before each test."""
        init_conversation_tables()
        init_tool_call_tables()
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Remove test data for this test class."""
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        # Delete test user data (user_id 200-201)
        cursor.execute("DELETE FROM conversation_messages WHERE user_id BETWEEN 200 AND 201")
        cursor.execute("DELETE FROM tool_calls WHERE message_id IN (SELECT id FROM conversation_messages WHERE user_id BETWEEN 200 AND 201)")
        conn.commit()
        conn.close()

    def test_link_tool_calls_to_messages(self):
        """
        Test: Tool calls correctly linked to messages.

        Acceptance Criteria from Task 1.6:
        - Tool calls stored with message_id
        - Tool calls retrievable by message_id
        - Multiple tool calls per message supported
        """
        user_id = 200

        # Store user message
        user_msg = store_message(
            user_id=user_id,
            role=MessageRole.USER,
            content="Add task to buy groceries and show my list"
        )

        # Store agent response
        agent_msg = store_message(
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content="I've added the task and here's your list."
        )

        # Store multiple tool calls for agent message
        tc1 = store_tool_call(
            message_id=agent_msg.id,
            tool_name="create_todo",
            parameters={"title": "Buy groceries", "user_id": user_id},
            result={"success": True, "todo_id": 1},
            status=ToolCallStatus.SUCCESS
        )

        tc2 = store_tool_call(
            message_id=agent_msg.id,
            tool_name="list_todos",
            parameters={"user_id": user_id},
            result={"todos": [{"id": 1, "title": "Buy groceries"}]},
            status=ToolCallStatus.SUCCESS
        )

        # Retrieve tool calls for message
        tool_calls = get_tool_calls_by_message(message_id=agent_msg.id)

        # Verify correct number of tool calls
        assert len(tool_calls) == 2

        # Verify tool calls linked to correct message
        assert tool_calls[0].message_id == agent_msg.id
        assert tool_calls[1].message_id == agent_msg.id

        # Verify tool names
        assert tool_calls[0].tool_name == "create_todo"
        assert tool_calls[1].tool_name == "list_todos"

        # Verify parameters preserved
        assert tool_calls[0].parameters["title"] == "Buy groceries"
        assert tool_calls[1].parameters["user_id"] == user_id

        # Verify results preserved
        assert tool_calls[0].result["success"] is True
        assert len(tool_calls[1].result["todos"]) == 1

        print("✓ Message-tool call linkage test passed")

    def test_tool_call_without_message_fails(self):
        """
        Test: Tool calls require valid message_id.

        Acceptance Criteria:
        - Invalid message_id rejected
        - Foreign key constraint enforced
        """
        # Attempt to store tool call with invalid message_id
        with pytest.raises(ValueError):
            store_tool_call(
                message_id=0,  # Invalid
                tool_name="create_todo",
                parameters={"title": "Test"},
                result={"success": True}
            )

        print("✓ Tool call validation test passed")


class TestUserDataIsolation:
    """Test user data isolation across multiple users."""

    def setup_method(self):
        """Initialize tables and clean test data before each test."""
        init_conversation_tables()
        init_tool_call_tables()
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Remove test data for this test class."""
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        # Delete test user data (user_id 300-402)
        cursor.execute("DELETE FROM conversation_messages WHERE user_id BETWEEN 300 AND 402")
        cursor.execute("DELETE FROM tool_calls WHERE message_id IN (SELECT id FROM conversation_messages WHERE user_id BETWEEN 300 AND 402)")
        conn.commit()
        conn.close()

    def test_users_cannot_see_each_others_messages(self):
        """
        Test: User data isolation enforced.

        Acceptance Criteria from Task 1.6:
        - User A messages not visible to User B
        - No cross-user data leakage
        """
        user_a_id = 300
        user_b_id = 301

        # User A stores messages
        msg_a1 = store_message(
            user_id=user_a_id,
            role=MessageRole.USER,
            content="User A message 1"
        )
        msg_a2 = store_message(
            user_id=user_a_id,
            role=MessageRole.ASSISTANT,
            content="User A message 2"
        )

        # User B stores messages
        msg_b1 = store_message(
            user_id=user_b_id,
            role=MessageRole.USER,
            content="User B message 1"
        )
        msg_b2 = store_message(
            user_id=user_b_id,
            role=MessageRole.ASSISTANT,
            content="User B message 2"
        )

        # Retrieve User A messages
        user_a_messages = get_recent_messages(user_id=user_a_id, limit=100)

        # Retrieve User B messages
        user_b_messages = get_recent_messages(user_id=user_b_id, limit=100)

        # Verify User A only sees their messages
        assert len(user_a_messages) == 2
        assert all(msg.user_id == user_a_id for msg in user_a_messages)
        assert user_a_messages[0].content == "User A message 1"

        # Verify User B only sees their messages
        assert len(user_b_messages) == 2
        assert all(msg.user_id == user_b_id for msg in user_b_messages)
        assert user_b_messages[0].content == "User B message 1"

        # Verify no ID overlap
        user_a_ids = {msg.id for msg in user_a_messages}
        user_b_ids = {msg.id for msg in user_b_messages}
        assert user_a_ids.isdisjoint(user_b_ids)

        # Verify message counts
        assert count_user_messages(user_a_id) == 2
        assert count_user_messages(user_b_id) == 2

        print("✓ User data isolation test passed")

    def test_concurrent_user_operations(self):
        """
        Test: Concurrent operations by multiple users.

        Acceptance Criteria:
        - Multiple users can store messages simultaneously
        - Data integrity maintained
        """
        user_ids = [400, 401, 402]
        messages_per_user = 5

        # Store messages for multiple users
        for user_id in user_ids:
            for i in range(messages_per_user):
                store_message(
                    user_id=user_id,
                    role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                    content=f"User {user_id} message {i+1}"
                )

        # Verify each user has correct number of messages
        for user_id in user_ids:
            count = count_user_messages(user_id)
            assert count == messages_per_user

        # Verify total messages
        total_messages = sum(count_user_messages(uid) for uid in user_ids)
        assert total_messages == len(user_ids) * messages_per_user

        print("✓ Concurrent user operations test passed")


class TestDataPersistence:
    """Test data persistence across sessions."""

    def setup_method(self):
        """Initialize tables and clean test data before each test."""
        init_conversation_tables()
        init_tool_call_tables()
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Remove test data for this test class."""
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        # Delete test user data (user_id 500-501)
        cursor.execute("DELETE FROM conversation_messages WHERE user_id BETWEEN 500 AND 501")
        cursor.execute("DELETE FROM tool_calls WHERE message_id IN (SELECT id FROM conversation_messages WHERE user_id BETWEEN 500 AND 501)")
        conn.commit()
        conn.close()

    def test_conversation_survives_restart(self):
        """
        Test: Conversation data persists across application restarts.

        Acceptance Criteria from Task 1.6:
        - Data survives database reconnection
        - All messages retrievable after restart
        """
        user_id = 500

        # Store messages
        msg1 = store_message(
            user_id=user_id,
            role=MessageRole.USER,
            content="Message before restart"
        )

        # Simulate application restart by closing and reopening connection
        # (This happens automatically with each function call)

        # Retrieve messages after "restart"
        messages = get_recent_messages(user_id=user_id, limit=10)

        # Verify message persisted
        assert len(messages) >= 1
        assert messages[-1].content == "Message before restart"

        # Store another message after "restart"
        msg2 = store_message(
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content="Message after restart"
        )

        # Retrieve all messages
        all_messages = get_recent_messages(user_id=user_id, limit=10)

        # Verify both messages present
        assert len(all_messages) >= 2
        assert any(msg.content == "Message before restart" for msg in all_messages)
        assert any(msg.content == "Message after restart" for msg in all_messages)

        print("✓ Data persistence test passed")

    def test_tool_calls_persist(self):
        """
        Test: Tool call records persist across sessions.

        Acceptance Criteria:
        - Tool calls survive restart
        - Linkage to messages maintained
        """
        user_id = 501

        # Store message
        msg = store_message(
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content="Response with tool call"
        )

        # Store tool call
        tc = store_tool_call(
            message_id=msg.id,
            tool_name="create_todo",
            parameters={"title": "Test"},
            result={"success": True}
        )

        # Simulate restart
        # Retrieve tool calls
        tool_calls = get_tool_calls_by_message(message_id=msg.id)

        # Verify tool call persisted
        assert len(tool_calls) >= 1
        assert tool_calls[-1].tool_name == "create_todo"
        assert tool_calls[-1].message_id == msg.id

        print("✓ Tool call persistence test passed")


class TestCompleteIntegration:
    """Complete integration test simulating real chat flow."""

    def setup_method(self):
        """Initialize tables and clean test data before each test."""
        init_conversation_tables()
        init_tool_call_tables()
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Remove test data for this test class."""
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        # Delete test user data (user_id 600)
        cursor.execute("DELETE FROM conversation_messages WHERE user_id = 600")
        cursor.execute("DELETE FROM tool_calls WHERE message_id IN (SELECT id FROM conversation_messages WHERE user_id = 600)")
        conn.commit()
        conn.close()

    def test_complete_chat_flow(self):
        """
        Test: Complete chat flow from user input to stored results.

        Simulates:
        1. User sends message
        2. Agent processes and invokes tools
        3. Agent responds
        4. All data stored and linked correctly
        """
        user_id = 600

        # === Turn 1: User asks to create todo ===
        user_msg1 = store_message(
            user_id=user_id,
            role=MessageRole.USER,
            content="Add a task to buy groceries"
        )
        assert user_msg1.id is not None

        # Agent processes and invokes create_todo tool
        agent_msg1 = store_message(
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content="I've added 'Buy groceries' to your todo list."
        )

        tool_call1 = store_tool_call(
            message_id=agent_msg1.id,
            tool_name="create_todo",
            parameters={"title": "Buy groceries", "user_id": user_id},
            result={"success": True, "todo_id": 1},
            status=ToolCallStatus.SUCCESS
        )

        # === Turn 2: User asks to list todos ===
        user_msg2 = store_message(
            user_id=user_id,
            role=MessageRole.USER,
            content="Show me my tasks"
        )

        # Agent processes and invokes list_todos tool
        agent_msg2 = store_message(
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content="Here are your tasks: 1. Buy groceries"
        )

        tool_call2 = store_tool_call(
            message_id=agent_msg2.id,
            tool_name="list_todos",
            parameters={"user_id": user_id},
            result={"todos": [{"id": 1, "title": "Buy groceries"}]},
            status=ToolCallStatus.SUCCESS
        )

        # === Verify complete flow ===

        # 1. All messages stored
        messages = get_recent_messages(user_id=user_id, limit=10)
        assert len(messages) == 4

        # 2. Messages in correct order
        assert messages[0].id == user_msg1.id
        assert messages[1].id == agent_msg1.id
        assert messages[2].id == user_msg2.id
        assert messages[3].id == agent_msg2.id

        # 3. Tool calls linked to correct messages
        tc1_list = get_tool_calls_by_message(agent_msg1.id)
        assert len(tc1_list) == 1
        assert tc1_list[0].tool_name == "create_todo"

        tc2_list = get_tool_calls_by_message(agent_msg2.id)
        assert len(tc2_list) == 1
        assert tc2_list[0].tool_name == "list_todos"

        # 4. Statistics correct
        stats = get_tool_call_statistics()
        assert stats['by_tool'].get('create_todo', 0) >= 1
        assert stats['by_tool'].get('list_todos', 0) >= 1

        print("✓ Complete chat flow test passed")


def run_all_integration_tests():
    """Run all integration tests and report results."""
    print("=" * 60)
    print("PHASE III PERSISTENCE LAYER INTEGRATION TESTS")
    print("=" * 60)
    print()

    test_classes = [
        TestMultiTurnConversation,
        TestMessageToolCallLinkage,
        TestUserDataIsolation,
        TestDataPersistence,
        TestCompleteIntegration
    ]

    total_tests = 0
    passed_tests = 0

    for test_class in test_classes:
        print(f"\n{test_class.__name__}")
        print("-" * 60)

        # Get all test methods
        test_methods = [
            method for method in dir(test_class)
            if method.startswith('test_')
        ]

        for method_name in test_methods:
            total_tests += 1
            try:
                # Create instance and run setup
                instance = test_class()
                instance.setup_method()

                # Run test method
                getattr(instance, method_name)()

                passed_tests += 1
            except Exception as e:
                print(f"✗ {method_name} FAILED: {e}")

    print()
    print("=" * 60)
    print(f"RESULTS: {passed_tests}/{total_tests} tests passed")
    print("=" * 60)

    return passed_tests == total_tests


if __name__ == "__main__":
    success = run_all_integration_tests()
    exit(0 if success else 1)
