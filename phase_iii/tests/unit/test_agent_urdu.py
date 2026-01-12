import pytest
from phase_iii.agent.agent import TodoAgent

def test_urdu_detection():
    agent = TodoAgent()
    assert agent.is_urdu("دودھ خریدیں") == True
    assert agent.is_urdu("Buy milk") == False
    assert agent.is_urdu("123") == False

def test_list_todos_urdu():
    agent = TodoAgent()
    response = agent.process_message("میری فہرست دکھائیں", [], 1)
    assert response["requires_tool_execution"] == True
    assert response["tool_calls"][0]["name"] == "list_todos"
    assert "فہرست" in response["response_text"]

def test_add_todo_urdu_variations():
    agent = TodoAgent()
    # Test different verbs for ADD
    variations = ["دودھ خریدنا شامل کرو", "بazar جانا ڈالو", "کتاب پڑھنا اضافہ کرو"]
    for msg in variations:
        response = agent.process_message(msg, [], 1)
        assert response["requires_tool_execution"] == True
        assert response["tool_calls"][0]["name"] == "create_todo"
        assert response["tool_calls"][0]["input"]["title"] in msg

def test_list_todos_urdu_variations():
    agent = TodoAgent()
    # Test different verbs for LIST
    variations = ["کاموں کی فہرست دکھاؤ", "میری لسٹ دکھائیں", "کیا ہیں میرے کام"]
    for msg in variations:
        response = agent.process_message(msg, [], 1)
        assert response["requires_tool_execution"] == True
        assert response["tool_calls"][0]["name"] == "list_todos"

def test_ordinal_parsing_urdu():
    agent = TodoAgent()
    # Test ordinals: پہلا -> 1, دوسرا -> 2
    response1 = agent.process_message("پہلا کام مکمل کرو", [], 1)
    assert response1["tool_calls"][0]["input"]["todo_id"] == 1
    assert response1["tool_calls"][0]["input"]["completed"] == True

    response2 = agent.process_message("دوسرا کام حذف کرو", [], 1)
    assert response2["tool_calls"][0]["input"]["todo_id"] == 2
    assert response2["tool_calls"][0]["name"] == "delete_todo"

def test_normalization_urdu():
    agent = TodoAgent()
    # Test with punctuation
    response = agent.process_message("دودھ خریدنا شامل کریں!", [], 1)
    assert "دودھ خریدنا" in response["response_text"]
    assert response["tool_calls"][0]["input"]["title"] == "دودھ خریدنا"
