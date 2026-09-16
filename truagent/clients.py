"""Model clients. Any OpenAI-compatible endpoint works out of the box.

TruAgent talks to Ollama, OpenAI, Anthropic (via their compatible layer),
vLLM, LM Studio, Together, Groq, ... using only the standard library
(``urllib``). No ``requests``, no ``httpx``, no SDKs.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .errors import APIError
from .parse import ToolCall

DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o-mini"


@dataclass
class AssistantMessage:
    """A model reply: free text and/or a tool call."""

    text: str = ""
    tool_call: ToolCall | None = None


def _tool_call_from_payload(raw: dict[str, Any]) -> ToolCall | None:
    """Build a ToolCall from one raw ``tool_calls[0]`` entry."""
    function = raw.get("function")
    if not isinstance(function, dict):
        return None
    name = function.get("name")
    if not isinstance(name, str) or not name:
        return None
    arguments = json.loads(function.get("arguments", "{}")) if isinstance(
        function.get("arguments"), str
    ) else (function.get("arguments") or {})
    call_id = raw.get("id") if isinstance(raw.get("id"), str) else None
    return ToolCall(name=name, arguments=arguments or {}, id=call_id)


class BaseLLM(ABC):
    """Minimal interface every backend implements."""

    @abstractmethod
    def chat(self, messages: list[Mapping[str, Any]]) -> AssistantMessage:
        """Send a conversation and return the assistant's reply."""


class OpenAICompatibleClient(BaseLLM):
    """A urllib-based client for any OpenAI-compatible chat-completions API."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        model: str = DEFAULT_MODEL,
        timeout: float = 30.0,
        retries: int = 0,
        max_tokens: int | None = None,
        temperature: float | None = None,
        stop: Sequence[str] | None = None,
        extra_headers: Mapping[str, str] | None = None,
        retry_delay: float = 0.1,
    ) -> None:
        if not isinstance(model, str) or not model:
            raise ValueError("model must be a non-empty string")
        if not isinstance(base_url, str) or not base_url:
            raise ValueError("base_url must be a non-empty string")
        if retries < 0:
            raise ValueError("retries must be a non-negative integer")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.retries = retries
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.stop = list(stop) if stop else None
        self.extra_headers = dict(extra_headers) if extra_headers else None
        self.retry_delay = retry_delay

    def chat(self, messages: list[Mapping[str, Any]]) -> AssistantMessage:
        payload: dict[str, Any] = {"model": self.model, "messages": list(messages)}
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.stop:
            payload["stop"] = self.stop
        tools = _collect_tools(messages)
        if tools:
            payload["tools"] = tools
        body = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
        headers = self._build_headers()
        last_error: BaseException | None = None
        for attempt in range(self.retries + 1):
            try:
                data = self._post(body, headers)
                return self._parse_response(data)
            except APIError as exc:
                # Don't retry client errors (4xx); retry 5xx and network failures.
                if exc.status_code is not None and 400 <= exc.status_code < 500:
                    raise
                last_error = exc
                if attempt < self.retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
                else:
                    raise
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                last_error = exc
                if attempt < self.retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
        raise APIError(f"model API unreachable: {last_error}", cause=last_error)

    def _build_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if self.extra_headers:
            headers.update(self.extra_headers)
        return headers

    def _post(self, body: bytes, headers: dict[str, str]) -> dict[str, Any]:
        base = self.base_url.rstrip("/")
        url = f"{base}/chat/completions"
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise APIError(
                f"HTTP {exc.code}: {detail}", status_code=exc.code, cause=exc
            ) from exc
        return json.loads(raw.decode("utf-8"))

    def _parse_response(self, data: dict[str, Any]) -> AssistantMessage:
        choices = data.get("choices")
        if not isinstance(choices, list) or not choices:
            raise APIError("model response contained no choices")
        message = choices[0].get("message") or {}
        content = message.get("content")
        text = content if isinstance(content, str) else ""
        tool_call: ToolCall | None = None
        raw_calls = message.get("tool_calls")
        if isinstance(raw_calls, list) and raw_calls:
            tool_call = _tool_call_from_payload(raw_calls[0])
        if not text and tool_call is None:
            raise APIError("model response contained no usable content")
        return AssistantMessage(text=text, tool_call=tool_call)

    def __repr__(self) -> str:
        return f"OpenAICompatibleClient(model={self.model!r}, base_url={self.base_url!r})"


def _collect_tools(messages: list[Mapping[str, Any]]) -> list[dict[str, Any]] | None:
    """Pull any tool definitions embedded in a message."""
    for message in messages:
        if isinstance(message, dict) and "tools" in message and isinstance(message["tools"], list):
            return message["tools"]
    return None


import time  # noqa: E402  (imported after helpers for clarity)