"""
Unit Tests for Voice Command Hooks

Verifies that process_voice_command correctly routes transcribed text
through the existing parsing logic.
"""

import pytest
from phase_iii.agent.agent import TodoAgent

def test_voice_routing_english():
    agent = TodoAgent()
    # Mock behavior of an STT engine output
    voice_input = "  add buy groceries  "
    response = agent.process_voice_command(voice_input, user_id=1)
    
    assert response["requires_tool_execution"] == True
    assert response["tool_calls"][0]["name"] == "create_todo"
    assert "groceries" in response["response_text"]

def test_voice_routing_urdu():
    agent = TodoAgent()
    # Mock behavior of an STT engine output (Urdu)
    voice_input = "دودھ خریدنا شامل کرو"
    response = agent.process_voice_command(voice_input, user_id=1)
    
    assert response["requires_tool_execution"] == True
    assert response["tool_calls"][0]["name"] == "create_todo"
    assert "دودھ خریدنا" in response["response_text"]

def test_voice_ordinal_routing_urdu():
    agent = TodoAgent()
    voice_input = "پہلا کام مکمل کرو"
    response = agent.process_voice_command(voice_input, user_id=1)
    
    assert response["tool_calls"][0]["input"]["todo_id"] == 1
    assert response["tool_calls"][0]["name"] == "update_todo"

def test_voice_normalization_reuse():
    agent = TodoAgent()
    # Voice input with trailing punctuation from STT
    voice_input = "میری فہرست دکھائیں؟"
    response = agent.process_voice_command(voice_input, user_id=1)
    
    assert response["requires_tool_execution"] == True
    assert response["tool_calls"][0]["name"] == "list_todos"
