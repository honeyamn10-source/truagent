"""Robust JSON parsing helpers for model output.

Models are notoriously sloppy with JSON. These helpers find the most likely
JSON object inside a blob of text, tolerate trailing commas, and coerce
tool-call arguments — the way a production agent actually needs.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

_TRAILING_COMMA_RE = re.compile(r",\s*([\]}])")


@dataclass
class ToolCall:
    """A parsed tool invocation from model output."""

    name: str
    arguments: dict[str, Any]
    id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize into the OpenAI-style ``tool_calls`` payload shape."""
        payload: dict[str, Any] = {
            "type": "function",
            "function": {
                "name": self.name,
                "arguments": json.dumps(self.arguments, ensure_ascii=False, default=str),
            },
        }
        if self.id:
            payload["id"] = self.id
        return payload


def repair_json(text: str) -> str | None:
    """Remove a single unambiguous trailing comma from invalid JSON.

    Returns the repaired text, or ``None`` if nothing safe to fix was found.
    """
    if not text:
        return None
    repaired, count = _TRAILING_COMMA_RE.subn(r"\1", text)
    if count == 1:
        return repaired
    return None


def _parse_with_repair(candidate: str) -> dict[str, Any] | None:
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass
    repaired = repair_json(candidate)
    if repaired is not None:
        try:
            return json.loads(repaired)
        except json.JSONDecodeError:
            pass
    return None


def extract_json(text: str) -> dict[str, Any] | None:
    """Extract the most relevant JSON object from model output.

    Priority order:
      1. A fenced `````json````` block.
      2. The outermost ``{...}`` span (with trailing-comma repair).
      3. ``None`` when nothing parseable exists.
    """
    if not text:
        return None
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidates: list[str] = []
    if fence:
        candidates.append(fence.group(1))
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        candidates.append(text[start : end + 1])
    for candidate in candidates:
        parsed = _parse_with_repair(candidate)
        if parsed is not None:
            return parsed
    return None


def parse_arguments(source: Any) -> dict[str, Any]:
    """Coerce a tool-call ``arguments`` field into a JSON object.

    Accepts: a dict (pass-through), a JSON string, or ``None``.
    """
    if source is None:
        return {}
    if isinstance(source, dict):
        return source
    if isinstance(source, str):
        parsed = _parse_with_repair(source.strip())
        if isinstance(parsed, dict):
            return parsed
        if parsed is None:
            return {"value": source}
        return {}
    return {}


def _from_openai_shape(obj: dict[str, Any]) -> ToolCall | None:
    function = obj.get("function")
    if not isinstance(function, dict):
        return None
    name = function.get("name")
    if not isinstance(name, str) or not name:
        return None
    arguments = parse_arguments(function.get("arguments"))
    call_id = obj.get("id") if isinstance(obj.get("id"), str) else None
    return ToolCall(name=name, arguments=arguments, id=call_id)


def _from_custom_shape(obj: dict[str, Any]) -> ToolCall | None:
    name = obj.get("tool") or obj.get("name")
    if not isinstance(name, str) or not name:
        return None
    return ToolCall(name=name, arguments=parse_arguments(obj.get("arguments")))


def extract_tool_call(text: str) -> ToolCall | None:
    """Extract a single ToolCall from raw model output.

    Tries the OpenAI ``tool_calls`` shape first, then a compact
    ``{"tool": ..., "arguments": ...}`` shape.
    """
    parsed = extract_json(text)
    if parsed is None:
        return None
    for key in ("tool_calls", "toolCall", "calls"):
        raw = parsed.get(key)
        if isinstance(raw, list) and raw:
            call = _from_openai_shape(raw[0])
            if call is not None:
                return call
    call = _from_custom_shape(parsed)
    if call is not None:
        return call
    if "tool" in parsed or "name" in parsed:
        return _from_custom_shape(parsed)
    return None


def iter_clean_json(text: str) -> Iterator[dict[str, Any]]:
    """Yield every JSON object found inside ``text`` (used for streaming logs)."""
    for match in re.finditer(r"\{.*?\}", text, re.DOTALL):
        parsed = _parse_with_repair(match.group(0))
        if parsed is not None:
            yield parsed