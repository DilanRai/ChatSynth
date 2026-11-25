from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

import requests

import openai_service


class FakeResponses:
    def __init__(self) -> None:
        self.last_request = None

    def create(self, **kwargs):
        self.last_request = kwargs
        return SimpleNamespace(
            output_text="hello from fake API",
            id="resp_test_123",
        )


class FakeClient:
    def __init__(self) -> None:
        self.responses = FakeResponses()


class FakeCompletions:
    def create(self, **kwargs):
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="hello from groq"))],
            id="chatcmpl_test_123",
        )


class FakeChat:
    def __init__(self) -> None:
        self.completions = FakeCompletions()


class FakeGroqClient:
    def __init__(self) -> None:
        self.chat = FakeChat()


class OpenAIServiceTests(unittest.TestCase):
    def test_gemini_response_uses_chat_completions(self) -> None:
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            text, response_id = openai_service._generate_gemini_response(
                "Hello",
                client=FakeGroqClient(),
            )

        self.assertEqual(text, "hello from groq")
        self.assertEqual(response_id, "chatcmpl_test_123")

    def test_nvidia_response_uses_chat_completions(self) -> None:
        with patch.dict("os.environ", {"NVIDIA_API_KEY": "test-key"}):
            text, response_id = openai_service._generate_nvidia_response(
                "Hello",
                client=FakeGroqClient(),
            )

        self.assertEqual(text, "hello from groq")
        self.assertEqual(response_id, "chatcmpl_test_123")

    def test_groq_response_uses_chat_completions(self) -> None:
        with patch.dict("os.environ", {"GROQ_API_KEY": "test-key"}):
            text, response_id = openai_service._generate_groq_response(
                "Hello",
                previous_messages=[{"role": "assistant", "content": "Hi"}],
                client=FakeGroqClient(),
            )

        self.assertEqual(text, "hello from groq")
        self.assertEqual(response_id, "chatcmpl_test_123")

    def test_openrouter_rate_limit_has_actionable_message(self) -> None:
        response = requests.Response()
        response.status_code = 429
        response.url = "https://openrouter.ai/api/v1/chat/completions"
        response.headers["Retry-After"] = "30"

        with (
            patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}),
            patch("openai_service.requests.post", return_value=response),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "rate limit reached.*Retry after 30 seconds",
            ):
                openai_service._generate_openrouter_response(
                    "Hello",
                    model="example/model:free",
                )

    def test_uses_responses_api_contract(self) -> None:
        client = FakeClient()

        text, response_id = openai_service.generate_response(
            "Hello",
            model="gpt-5.5",
            client=client,
        )

        self.assertEqual(text, "hello from fake API")
        self.assertEqual(response_id, "resp_test_123")
        self.assertEqual(client.responses.last_request["model"], "gpt-5.5")
        self.assertEqual(client.responses.last_request["input"], "Hello")
        self.assertIn("instructions", client.responses.last_request)
        self.assertNotIn(
            "previous_response_id",
            client.responses.last_request,
        )

    def test_previous_response_id_is_forwarded(self) -> None:
        client = FakeClient()

        openai_service.generate_response(
            "Follow up",
            previous_response_id="resp_previous",
            client=client,
        )

        self.assertEqual(
            client.responses.last_request["previous_response_id"],
            "resp_previous",
        )

    def test_empty_prompt_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            openai_service.generate_response(
                "   ",
                client=FakeClient(),
            )


if __name__ == "__main__":
    unittest.main()
