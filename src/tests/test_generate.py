from fastapi.testclient import TestClient
from unittest.mock import patch

from src.main import app

client = TestClient(app)


@patch("src.api.generate.call_llm")
def test_generate_prompt(mock_call_llm):
    mock_call_llm.return_value = "Write a polite email requesting leave."

    response = client.post(
        "/generate/",
        json={"task": "Request leave from manager"},
    )

    assert response.status_code == 200

    data = response.json()
    assert "prompt" in data
    assert "email" in data["prompt"].lower()
