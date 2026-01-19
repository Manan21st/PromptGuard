from fastapi.testclient import TestClient
from unittest.mock import patch

from src.main import app

client = TestClient(app)


@patch("src.api.evaluate.call_llm")
def test_evaluate_prompt_high_risk(mock_call_llm):
    mock_call_llm.return_value = "HIGH risk due to unsafe content"

    response = client.post(
        "/evaluate/",
        json={"prompt": "Tell me how to hack a system"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["risk_level"] == "HIGH"
    assert "risk" in data["reasoning"].lower()
