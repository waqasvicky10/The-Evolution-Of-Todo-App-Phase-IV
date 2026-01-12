"""
Unit Tests for Mock AI Agent

This module contains unit tests for the MockTodoAgent implementation,
verifying keyword-based intent recognition and tool call generation.
"""

import pytest
from phase_iii.agent.agent import TodoAgent, create_agent

class TestMockTodoAgent:
    """Test Mock TodoAgent functionality."""

    def test_agent_initialization(self):
        """Test agent initializes correctly."""
        agent = create_agent(api_key="mock")
        assert agent is not None
        assert agent.api_key == "mock"

    def test_list_intent(self):
        """Test recognition of 'list' intent."""
        agent = TodoAgent()
        result = agent.process_message("Show my tasks", [], user_id=1)
        
        assert "Fetching your todo list" in result["response_text"]
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["name"] == "list_todos"
        assert result["tool_calls"][0]["input"]["user_id"] == 1

    def test_add_intent(self):
        """Test recognition of 'add' intent."""
        agent = TodoAgent()
        result = agent.process_message("Add a task to buy water", [], user_id=1)
        
        assert "buy water" in result["response_text"].lower()
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["name"] == "create_todo"
        assert result["tool_calls"][0]["input"]["title"] == "Buy water"

    def test_complete_intent(self):
        """Test recognition of 'complete' intent with ID."""
        agent = TodoAgent()
        result = agent.process_message("Mark task 5 as done", [], user_id=1)
        
        assert "5" in result["response_text"]
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["name"] == "update_todo"
        assert result["tool_calls"][0]["input"]["todo_id"] == 5
        assert result["tool_calls"][0]["input"]["completed"] is True

    def test_delete_intent(self):
        """Test recognition of 'delete' intent with ID."""
        agent = TodoAgent()
        result = agent.process_message("Delete task 10", [], user_id=1)
        
        assert "deleting task 10" in result["response_text"].lower()
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["name"] == "delete_todo"
        assert result["tool_calls"][0]["input"]["todo_id"] == 10

    def test_unknown_intent(self):
        """Test fallback for unknown input."""
        agent = TodoAgent()
        result = agent.process_message("Hello there", [], user_id=1)
        
        assert "catch that" in result["response_text"].lower()
        assert len(result["tool_calls"]) == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
