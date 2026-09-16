"""Tests for the urllib-based OpenAICompatibleClient (no network required)."""

from __future__ import annotations

import io
import json
import urllib.error

import pytest
from conftest import add, double

from truagent import APIError, AssistantMessage, BaseLLM, OpenAICompatibleClient


class StubResponse:
    def __init__(self, data: bytes, code: int = 200) -> None:
        self._data = data
        self.code = code

    def read(self) -> bytes:
        if self.code != 200:
            raise urllib.error.HTTPError(
                "url", self.code, "error", {}, io.BytesIO(self._data)
            )
        return self._data


class StubOpener:
    """Mimics urllib.request for injection."""

    def __init__(self, responses) -> None:
        self._responses = list(responses)
        self.calls: list = []

    def urlopen(self, request, timeout=None):  # noqa: ANN001
        self.calls.append((request.full_url, request.data, dict(request.headers.items())))
        if not self._responses:
            raise urllib.error.URLError("no response queued")
        response = self._responses.pop(0)
        if isinstance(response, urllib.error.URLError):
            raise response
        return response


def build_client(responses, **kwargs) -> tuple:
    opener = StubOpener(responses)
    client = OpenAICompatibleClient(api_key="test-key", base_url="https://api.example.com/v1", **kwargs)
    client._post = lambda body, headers: _via_opener(opener, client, body, headers)
    return client, opener


def _via_opener(opener, client, body, headers):  # noqa: ANN001
    from urllib.request import Request

    base = client.base_url.rstrip("/")
    request = Request(
        f"{base}/chat/completions",
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        resp = opener.urlopen(request)
    except urllib.error.HTTPError as exc:
        from truagent import APIError

        raise APIError(f"HTTP {exc.code}: {exc}", status_code=exc.code, cause=exc) from exc
    return json.loads(resp.read())


def _chat_response(text="", tool_calls=None) -> StubResponse:
    message: dict = {"role": "assistant"}
    if text:
        message["content"] = text
    if tool_calls:
        message["tool_calls"] = tool_calls
    payload = {"choices": [{"message": message}]}
    return StubResponse(json.dumps(payload).encode("utf-8"))


def test_chat_returns_text_message() -> None:
    client, opener = build_client([_chat_response(text="Hello!")])
    reply = client.chat([{"role": "user", "content": "hi"}])
    assert isinstance(reply, AssistantMessage)
    assert reply.text == "Hello!"
    assert reply.tool_call is None


def test_chat_parses_tool_calls() -> None:
    tool_calls = [
        {
            "id": "call_1",
            "type": "function",
            "function": {"name": "add", "arguments": json.dumps({"x": 1, "y": 2})},
        }
    ]
    client, _ = build_client([_chat_response(tool_calls=tool_calls)])
    reply = client.chat([{"role": "user", "content": "add"}])
    assert reply.tool_call is not None
    assert reply.tool_call.name == "add"
    assert reply.tool_call.arguments == {"x": 1, "y": 2}


def test_payload_includes_model_and_options() -> None:
    client, opener = build_client(
        [_chat_response(text="ok")],
        model="test-model",
        max_tokens=100,
        temperature=0.5,
        stop=["END"],
    )
    client.chat([{"role": "user", "content": "hi"}])
    _, raw_body, _ = opener.calls[0]
    payload = json.loads(raw_body)
    assert payload["model"] == "test-model"
    assert payload["max_tokens"] == 100
    assert payload["temperature"] == 0.5
    assert payload["stop"] == ["END"]


def test_request_url_and_headers() -> None:
    client, opener = build_client([_chat_response(text="ok")])
    client.chat([{"role": "user", "content": "hi"}])
    url, _, headers = opener.calls[0]
    assert url.endswith("/chat/completions")
    assert headers.get("Authorization") == "Bearer test-key"
    assert headers.get("Content-Type") == "application/json" or headers.get(
        "Content-type"
    ) == "application/json"


def test_no_auth_header_without_api_key() -> None:
    client, opener = build_client([_chat_response(text="ok")])
    client.api_key = None
    client.chat([{"role": "user", "content": "hi"}])
    _, _, headers = opener.calls[0]
    assert "Authorization" not in headers


def test_trailing_slash_on_base_url_tolerated() -> None:
    client, opener = build_client([_chat_response(text="ok")])
    client.base_url = "https://api.example.com/v1/"
    client.chat([{"role": "user", "content": "hi"}])
    url, _, _ = opener.calls[0]
    assert "//chat/completions" not in url


def test_transient_network_error_is_retried() -> None:
    client, opener = build_client(
        [urllib.error.URLError("boom"), _chat_response(text="recovered")],
        retries=2,
    )
    reply = client.chat([{"role": "user", "content": "hi"}])
    assert reply.text == "recovered"
    assert len(opener.calls) == 2


def test_retry_exhaustion_raises_api_error() -> None:
    client, _ = build_client(
        [urllib.error.URLError("boom"), urllib.error.URLError("boom")],
        retries=1,
    )
    with pytest.raises(APIError):
        client.chat([{"role": "user", "content": "hi"}])


def test_http_error_raises_immediately_with_status() -> None:
    err = urllib.error.HTTPError("url", 429, "rate limited", {}, io.BytesIO(b"slow down"))
    client, _ = build_client([err], retries=3)
    with pytest.raises(APIError) as exc_info:
        client.chat([{"role": "user", "content": "hi"}])
    assert exc_info.value.status_code == 429


def test_no_choices_raises() -> None:
    bad = StubResponse(json.dumps({"choices": []}).encode("utf-8"))
    client, _ = build_client([bad])
    with pytest.raises(APIError):
        client.chat([{"role": "user", "content": "hi"}])


def test_empty_message_raises() -> None:
    bad = StubResponse(
        json.dumps({"choices": [{"message": {"role": "assistant", "content": ""}}]}).encode("utf-8")
    )
    client, _ = build_client([bad])
    with pytest.raises(APIError):
        client.chat([{"role": "user", "content": "hi"}])


def test_validation() -> None:
    with pytest.raises(ValueError):
        OpenAICompatibleClient(model="")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        OpenAICompatibleClient(retries=-1)
    with pytest.raises(ValueError):
        OpenAICompatibleClient(base_url="")


def test_base_llm_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        BaseLLM()  # type: ignore[abstract]


def test_schemas_exported_from_client_tools() -> None:
    from truagent.tools import ToolRegistry

    registry = ToolRegistry([add, double])
    assert len(registry.schemas()) == 2