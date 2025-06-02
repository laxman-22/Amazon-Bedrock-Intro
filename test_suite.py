import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from fast_api import app, rds

client = TestClient(app)

session_id = "test-session"
mock_user_input = "What's the capital of France?"
mock_model_output = "The capital of France is Paris."

@pytest.fixture(autouse=True)
def clear_redis_before_test():
    rds.delete(session_id)
    yield
    rds.delete(session_id)

# Helper to mock Bedrock streaming response
class MockStream:
    def __init__(self, json_obj):
        self.json_obj = json_obj

    def read(self):
        return json.dumps(self.json_obj).encode("utf-8")

@patch("fast_api.brt.invoke_model")
def test_chat_success(mock_bedrock):
    mock_bedrock.return_value = {
        "body": MockStream({
            "content": [{"type": "text", "text": mock_model_output}]
        })
    }

    response = client.post("/chat", json={
        "user_input": mock_user_input,
        "session_id": session_id
    })

    assert response.status_code == 200
    data = response.json()
    assert "res" in data
    assert mock_model_output in data["res"]

    # Verify Redis stored history
    history = json.loads(rds.get(session_id))
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"

@patch("fast_api.brt.invoke_model")
def test_chat_missing_input(mock_bedrock):
    response = client.post("/chat", json={
        "session_id": session_id
    })
    assert response.status_code == 422

@patch("fast_api.brt.invoke_model")
def test_clear_session(mock_bedrock):
    rds.set(session_id, json.dumps([
        {"role": "user", "content": [{"type": "text", "text": "hi"}]}
    ]))

    response = client.post("/clear", json={
        "user_input": "",
        "session_id": session_id
    })

    assert response.status_code == 200
    assert response.json() == {"res": "success"}
    assert rds.get(session_id) is None

@patch("fast_api.brt.invoke_model")
def test_chat_multiple_turns(mock_bedrock):
    mock_bedrock.return_value = {
        "body": MockStream({
            "content": [{"type": "text", "text": mock_model_output}]
        })
    }

    # Turn 1
    res1 = client.post("/chat", json={
        "user_input": mock_user_input,
        "session_id": session_id
    })
    assert res1.status_code == 200

    # Turn 2
    res2 = client.post("/chat", json={
        "user_input": "What about Germany?",
        "session_id": session_id
    })
    assert res2.status_code == 200

    history = json.loads(rds.get(session_id))
    assert len(history) == 4
    roles = [msg["role"] for msg in history]
    assert roles == ["user", "assistant", "user", "assistant"]

@patch("fast_api.brt.invoke_model", side_effect=Exception("Bedrock failure"))
def test_bedrock_failure_handling(mock_bedrock):
    response = client.post("/chat", json={
        "user_input": "trigger error",
        "session_id": session_id
    })
    assert response.status_code == 200
    assert "error" in response.json()