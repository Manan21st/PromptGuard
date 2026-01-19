import os
from google import genai

class LLMClientError(RuntimeError):
    """Raised when LLM client is misconfigured or fails."""


def _get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise LLMClientError("GEMINI_API_KEY environment variable is not set")

    return genai.Client(api_key=api_key)


def call_llm(prompt: str) -> str:
    """
    Calls Gemini LLM with the given prompt and returns generated text.
    This function is intentionally isolated for easy mocking in tests.
    """
    client = _get_client()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
    except Exception as exc:
        raise LLMClientError(f"LLM call failed: {exc}") from exc

    if not response or not response.text:
        raise LLMClientError("Empty response received from LLM")

    return response.text.strip()
