from __future__ import annotations

import os
from typing import Any

import requests
from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct")
API_PROVIDER = os.getenv("API_PROVIDER", "openai").lower()

DEFAULT_INSTRUCTIONS = (
    "You are a helpful AI assistant. Be accurate, concise, and explicit when "
    "you are uncertain."
)


def _require_api_key() -> None:
    """Check if the appropriate API key is set based on the provider."""
    if API_PROVIDER in {"openrouter", "groq", "gemini", "nvidia"}:
        key_name = {
            "openrouter": "OPENROUTER_API_KEY",
            "groq": "GROQ_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "nvidia": "NVIDIA_API_KEY",
        }[API_PROVIDER]
        if not os.getenv(key_name):
            raise RuntimeError(
                f"{key_name} is not set. Store the API key in your environment; "
                "never commit it to source control."
            )
    else:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Store the API key in your environment; "
                "never commit it to source control."
            )


def _generate_openrouter_response(
    prompt: str,
    *,
    model: str | None = None,
    previous_messages: list[dict] | None = None,
) -> tuple[str, str]:
    """Generate response using OpenRouter API."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")
    
    # Build messages array
    messages = list(previous_messages or [])
    messages.append({"role": "user", "content": prompt})
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # Add optional site information for rankings
    site_url = os.getenv("OPENROUTER_SITE_URL")
    site_name = os.getenv("OPENROUTER_SITE_NAME")
    if site_url:
        headers["HTTP-Referer"] = site_url
    if site_name:
        headers["X-Title"] = site_name
    
    # Prepare request data
    data = {
        "model": model or OPENROUTER_MODEL,
        "messages": messages,
    }
    
    # Make API request
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=(10, 60),
    )
    
    # Check for errors
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            reset_at = response.headers.get("X-RateLimit-Reset")
            details = [
                "OpenRouter rate limit reached for this account or free-model quota."
            ]
            if retry_after:
                details.append(f"Retry after {retry_after} seconds.")
            elif reset_at:
                details.append(f"Rate limit reset: {reset_at}.")
            details.append(
                "Wait and try again, switch to OpenAI, or use a paid OpenRouter model."
            )
            raise RuntimeError(" ".join(details)) from exc
        raise
    
    # Parse response
    response_data = response.json()
    
    if "choices" not in response_data or len(response_data["choices"]) == 0:
        raise RuntimeError("OpenRouter API returned no choices.")
    
    message = response_data["choices"][0]["message"]
    output_text = (message.get("content") or "").strip()
    
    if not output_text:
        output_text = "[The API returned no text output.]"
    
    # Return output and a unique ID
    response_id = response_data.get("id", "")
    
    return output_text, response_id


def _generate_groq_response(
    prompt: str,
    *,
    model: str | None = None,
    previous_messages: list[dict] | None = None,
    client: Any | None = None,
) -> tuple[str, str]:
    """Generate a response using Groq's OpenAI-compatible API."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set.")

    if client is None:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

    messages = list(previous_messages or [])
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=model or GROQ_MODEL,
        messages=messages,
    )

    output_text = (response.choices[0].message.content or "").strip()
    if not output_text:
        output_text = "[The API returned no text output.]"

    return output_text, response.id


def _generate_gemini_response(
    prompt: str,
    *,
    model: str | None = None,
    previous_messages: list[dict] | None = None,
    client: Any | None = None,
) -> tuple[str, str]:
    """Generate a response using Gemini API's OpenAI-compatible endpoint."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    if client is None:
        client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    messages = list(previous_messages or [])
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=model or GEMINI_MODEL,
        messages=messages,
    )

    output_text = (response.choices[0].message.content or "").strip()
    if not output_text:
        output_text = "[The API returned no text output.]"

    return output_text, response.id


def _generate_nvidia_response(
    prompt: str,
    *,
    model: str | None = None,
    previous_messages: list[dict] | None = None,
    client: Any | None = None,
) -> tuple[str, str]:
    """Generate a response using NVIDIA NIM's OpenAI-compatible API."""
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY is not set.")

    if client is None:
        client = OpenAI(
            api_key=api_key,
            base_url="https://integrate.api.nvidia.com/v1",
        )

    messages = list(previous_messages or [])
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=model or NVIDIA_MODEL,
        messages=messages,
    )

    output_text = (response.choices[0].message.content or "").strip()
    if not output_text:
        output_text = "[The API returned no text output.]"

    return output_text, response.id


def _generate_openai_response(
    prompt: str,
    *,
    model: str | None = None,
    previous_response_id: str | None = None,
    client: Any | None = None,
) -> tuple[str, str]:
    """Generate response using OpenAI Responses API."""
    if client is None:
        client = OpenAI()

    request: dict[str, Any] = {
        "model": model or DEFAULT_MODEL,
        "instructions": DEFAULT_INSTRUCTIONS,
        "input": prompt,
    }

    if previous_response_id:
        request["previous_response_id"] = previous_response_id

    response = client.responses.create(**request)

    output_text = (response.output_text or "").strip()
    if not output_text:
        output_text = "[The API returned no text output.]"

    return output_text, response.id


def generate_response(
    prompt: str,
    *,
    model: str | None = None,
    previous_response_id: str | None = None,
    previous_messages: list[dict] | None = None,
    client: Any | None = None,
) -> tuple[str, str]:
    """
    Generate a response using the configured API provider.
    
    Args:
        prompt: User input text
        model: Model to use (provider-specific)
        previous_response_id: For OpenAI, the previous response ID
        previous_messages: For OpenRouter, Groq, Gemini, and NVIDIA, the conversation history
        client: Optional OpenAI client instance
        
    Returns:
        Tuple of (response_text, response_id)
    """
    cleaned_prompt = prompt.strip()
    if not cleaned_prompt:
        raise ValueError("Prompt must not be empty.")

    if client is None:
        _require_api_key()
    
    if API_PROVIDER == "openrouter":
        return _generate_openrouter_response(
            cleaned_prompt,
            model=model,
            previous_messages=previous_messages,
        )
    if API_PROVIDER == "groq":
        return _generate_groq_response(
            cleaned_prompt,
            model=model,
            previous_messages=previous_messages,
            client=client,
        )
    if API_PROVIDER == "gemini":
        return _generate_gemini_response(
            cleaned_prompt,
            model=model,
            previous_messages=previous_messages,
            client=client,
        )
    if API_PROVIDER == "nvidia":
        return _generate_nvidia_response(
            cleaned_prompt,
            model=model,
            previous_messages=previous_messages,
            client=client,
        )
    else:
        return _generate_openai_response(
            cleaned_prompt,
            model=model,
            previous_response_id=previous_response_id,
            client=client,
        )
