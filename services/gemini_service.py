"""Gemini client for the PM Opportunity Agent."""

from google import genai


class GeminiService:
    """Sends prompts to the Gemini API and returns the raw text response."""

    _MODEL = "gemini-2.5-flash"

    def __init__(self, api_key: str) -> None:
        """Initialize the Gemini client with the provided API key."""
        self._client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """Send a prompt to Gemini and return the raw text response unchanged."""
        response = self._client.models.generate_content(
            model=self._MODEL,
            contents=prompt,
        )
        return response.text
